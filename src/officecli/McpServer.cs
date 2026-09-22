<<<<<<< HEAD
// Copyright 2025 OfficeCLI (officecli.ai)
// SPDX-License-Identifier: Apache-2.0

using System.Reflection;
using System.Text;
using System.Text.Json;
=======
// Copyright 2026 OfficeCLI (https://OfficeCLI.AI)
// SPDX-License-Identifier: Apache-2.0

using System.CommandLine;
using System.Reflection;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
>>>>>>> upstream/main
using OfficeCli.Core;
using OfficeCli.Handlers;

namespace OfficeCli;

/// <summary>
/// Minimal MCP (Model Context Protocol) server over stdio.
/// Implements JSON-RPC 2.0 with initialize, tools/list, and tools/call.
/// All JSON is hand-written via Utf8JsonWriter to avoid reflection (PublishTrimmed).
/// </summary>
public static class McpServer
{
    public static async Task RunAsync()
    {
        using var reader = new StreamReader(Console.OpenStandardInput());
        using var writer = new StreamWriter(Console.OpenStandardOutput()) { AutoFlush = true };

<<<<<<< HEAD
=======
        // Default this stdio process to NOT auto-spawn a resident. This opts
        // out of spawning only — it does NOT bypass an existing one: TryResident
        // still routes through a resident another officecli already holds for the
        // file (probe-then-TrySend in CommandBuilder.TryResident), so two writers
        // never fight over the file and no update is lost. The effect of the
        // opt-out:
        //   - no resident holds the file -> the command opens, applies, and
        //     eager-saves directly, so the mutation is on disk by the time the
        //     response returns;
        //   - a resident already holds the file -> the command routes through it
        //     and follows that resident's deferred flush (on disk at its
        //     save/close/idle), same as any other client of that resident.
        // Defaulting the opt-out on keeps a lone MCP session from leaving a
        // spawned resident (and its deferred-flush surprise) behind it. An
        // explicit user value (e.g. to opt INTO spawning residents) is respected.
        if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("OFFICECLI_NO_AUTO_RESIDENT")))
            Environment.SetEnvironmentVariable("OFFICECLI_NO_AUTO_RESIDENT", "1");

        // The MCP process always has stdin redirected (it IS the JSON-RPC
        // channel), so `batch --commands/--input` would emit the "stdin is also
        // redirected; stdin will be ignored" warning on EVERY call — noise that
        // also lands in the result text and breaks naive JSON parsing of the
        // batch envelope. Under MCP that warning describes the transport, not a
        // user mistake, so default its existing opt-out on (respect any explicit
        // value).
        if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("OFFICECLI_BATCH_ALLOW_STDIN_REDIRECT")))
            Environment.SetEnvironmentVariable("OFFICECLI_BATCH_ALLOW_STDIN_REDIRECT", "1");

>>>>>>> upstream/main
        // MCP server is a long-lived stdio process. The normal
        // per-invocation auto-upgrade path (Program.cs:112) is
        // short-circuited for `officecli mcp` because CheckInBackground
        // is called AFTER the mcp branch in Program.cs — so without
        // this hook, an MCP instance started once and left running for
        // days/weeks would never see a new release.
        //
        // Run the upgrade path in the background: fire once at startup
        // (applies any pending .update from a previous run and kicks a
        // fresh check if >24h stale), then every hour. The hourly wake
        // is cheap because CheckInBackground is debounced by the same
        // 24h timestamp in ~/.officecli/config.json as the normal CLI
        // path, so 23 of 24 wakes no-op. The actual download / verify /
        // File.Move happens in a spawned subprocess whose stdio is
        // redirected (see UpdateChecker.SpawnRefreshProcess), so
        // nothing it does can corrupt our stdout JSON-RPC stream.
        using var upgradeCts = new CancellationTokenSource();
        var upgradeTask = RunPeriodicUpgradeCheckAsync(upgradeCts.Token);

        try
        {
            while (true)
            {
                var line = await reader.ReadLineAsync();
                if (line == null) break;
                if (string.IsNullOrWhiteSpace(line)) continue;

                JsonElement? id = null;
                try
                {
                    using var doc = JsonDocument.Parse(line);
                    var root = doc.RootElement;
                    // The JSON-RPC root must be an Object (single request). Arrays
                    // are valid JSON-RPC 2.0 batch requests that we don't support;
                    // numbers/strings/bools/nulls are malformed entirely. Guard
                    // here before TryGetProperty, which throws on non-Object.
                    if (root.ValueKind != JsonValueKind.Object)
                    {
                        var msg = root.ValueKind == JsonValueKind.Array
                            ? "Invalid Request: batch requests are not supported"
                            : "Invalid Request: request must be a JSON object";
                        await writer.WriteLineAsync(ErrorJson(null, -32600, msg));
                        continue;
                    }
                    // Parse id BEFORE method so a malformed method ('method': 42)
                    // can still echo the original id back per JSON-RPC 2.0 §5.
                    id = root.TryGetProperty("id", out var idEl) ? idEl.Clone() : null;
                    // method must be a string per spec; non-string is an
                    // Invalid Request (-32600), not an internal error.
                    string? method = null;
                    if (root.TryGetProperty("method", out var m))
                    {
                        if (m.ValueKind != JsonValueKind.String)
                        {
                            await writer.WriteLineAsync(ErrorJson(id, -32600, "Invalid Request: 'method' must be a string"));
                            continue;
                        }
                        method = m.GetString();
                    }

                    var response = method switch
                    {
                        "initialize" => HandleInitialize(id),
                        "notifications/initialized" => null,
                        "tools/list" => HandleToolsList(id),
                        "tools/call" => HandleToolsCall(id, root),
                        "ping" => WriteJson(w => { w.WriteStartObject(); Rpc(w, id); w.WriteStartObject("result"); w.WriteEndObject(); w.WriteEndObject(); }),
                        // CONSISTENCY(mcp-error): truncate caller-supplied value to prevent
                        // response amplification (echo arbitrary-length input back unchanged).
                        _ => id.HasValue ? ErrorJson(id, -32601, $"Method not found: {OfficeCli.Help.SchemaHelpLoader.TruncateForError(method ?? "", 64)}") : null,
                    };

                    if (response != null)
                        await writer.WriteLineAsync(response);
                }
                catch (JsonException)
                {
                    await writer.WriteLineAsync(ErrorJson(null, -32700, "Parse error"));
                }
                catch (Exception ex)
                {
                    await writer.WriteLineAsync(ErrorJson(id, -32603, $"Internal error: {ex.Message}"));
                }
            }
        }
        finally
        {
            upgradeCts.Cancel();
            try { await upgradeTask; } catch { }
        }
    }

    private static async Task RunPeriodicUpgradeCheckAsync(CancellationToken token)
    {
        // Fire once at startup — no matter what state the config is in,
        // this applies any pending .update from a previous run and
        // (if stale) spawns a fresh download. Does not block the main
        // loop: this method runs on a background task.
        try { UpdateChecker.CheckInBackground(); } catch { }

        while (!token.IsCancellationRequested)
        {
            try
            {
                await Task.Delay(TimeSpan.FromHours(1), token);
                UpdateChecker.CheckInBackground();
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch
            {
                // Never crash the MCP server over an update-check failure.
                // UpdateChecker already swallows exceptions internally, so
                // this is belt-and-braces for any future change that might
                // leak one through.
            }
        }
    }

    // ==================== Handlers ====================

    private static string HandleInitialize(JsonElement? id) => WriteJson(w =>
    {
        w.WriteStartObject();
        Rpc(w, id);
        w.WriteStartObject("result");
        w.WriteString("protocolVersion", "2024-11-05");
        w.WriteStartObject("capabilities");
        w.WriteStartObject("tools"); w.WriteBoolean("listChanged", false); w.WriteEndObject();
        w.WriteEndObject();
        var ver = Assembly.GetExecutingAssembly().GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion ?? "0.0.0";
        w.WriteStartObject("serverInfo"); w.WriteString("name", "officecli"); w.WriteString("version", ver); w.WriteEndObject();
        w.WriteEndObject();
        w.WriteEndObject();
    });

    private static string HandleToolsList(JsonElement? id) => WriteJson(w =>
    {
        w.WriteStartObject();
        Rpc(w, id);
        w.WriteStartObject("result");
        w.WriteStartArray("tools");
        WriteToolDefinitions(w);
        w.WriteEndArray();
        w.WriteEndObject();
        w.WriteEndObject();
    });

    private static string HandleToolsCall(JsonElement? id, JsonElement root)
    {
        if (!root.TryGetProperty("params", out var p))
            return ErrorJson(id, -32602, "Missing params");
        var name = p.TryGetProperty("name", out var n) ? n.GetString() : null;
        var args = p.TryGetProperty("arguments", out var a) ? a : default;
        if (string.IsNullOrEmpty(name))
            return ErrorJson(id, -32602, "Missing tool name");
<<<<<<< HEAD

        try
        {
            // Unified tool: route by "command" arg; legacy: route by tool name
            var toolName = name == "officecli" && args.ValueKind == JsonValueKind.Object && args.TryGetProperty("command", out var cmd)
                ? cmd.GetString() ?? name : name;
            var contents = ExecuteToolMulti(toolName, args);
=======
        // This server advertises exactly one tool. A misrouted call must not
        // silently execute (it would mutate files under a bogus tool name);
        // reject anything else the way an unknown tool should fail.
        if (name != "officecli")
            return ErrorJson(id, -32602, $"Unknown tool: {name}. This server exposes a single tool: officecli.");

        try
        {
            // Thin shell: the officecli tool takes a CLI command line in
            // `command` and runs it through the shared System.CommandLine root.
            var (contents, isError) = ExecuteCommandLine(args);
>>>>>>> upstream/main
            return WriteJson(w =>
            {
                w.WriteStartObject();
                Rpc(w, id);
                w.WriteStartObject("result");
                w.WriteStartArray("content");
                foreach (var c in contents)
                {
                    w.WriteStartObject();
                    w.WriteString("type", c.Type);
                    if (c.Text != null) w.WriteString("text", c.Text);
                    if (c.Data != null) w.WriteString("data", c.Data);
                    if (c.MimeType != null) w.WriteString("mimeType", c.MimeType);
                    w.WriteEndObject();
                }
                w.WriteEndArray();
<<<<<<< HEAD
                w.WriteBoolean("isError", false);
=======
                w.WriteBoolean("isError", isError);
>>>>>>> upstream/main
                w.WriteEndObject();
                w.WriteEndObject();
            });
        }
        catch (Exception ex)
        {
            return WriteJson(w =>
            {
                w.WriteStartObject();
                Rpc(w, id);
                w.WriteStartObject("result");
                w.WriteStartArray("content");
<<<<<<< HEAD
                w.WriteStartObject(); w.WriteString("type", "text"); w.WriteString("text", $"Error: {ex.Message}"); w.WriteEndObject();
=======
                // Only PRE-handler failures reach here now — argv extraction and
                // CLI parse/validation errors (the shared-grammar "free win"
                // messages). A handler that ran and exited non-zero (batch /
                // validate business verdicts) returns its stdout verbatim with
                // isError=true from ExecuteCommandLine, not via this path.
                var errText = $"Error: {ex.Message}";
                w.WriteStartObject(); w.WriteString("type", "text"); w.WriteString("text", errText); w.WriteEndObject();
>>>>>>> upstream/main
                w.WriteEndArray();
                w.WriteBoolean("isError", true);
                w.WriteEndObject();
                w.WriteEndObject();
            });
        }
    }

    // ==================== Tool Execution ====================

    /// <summary>
    /// MCP content block. Most tool responses are a single text block; screenshot
    /// returns a text caption + an image block (base64 PNG). Fields not relevant
    /// to a given Type are left null and omitted on serialization.
    /// </summary>
    private sealed record McpContent(string Type, string? Text = null, string? Data = null, string? MimeType = null);

<<<<<<< HEAD
    /// <summary>
    /// Multi-modal wrapper around <see cref="ExecuteTool"/>. Special-cases
    /// view+screenshot (returns text caption + base64 PNG); everything else
    /// gets the legacy single-text path. Lets us add image responses without
    /// touching the ~50 string-returning case branches.
    /// </summary>
    private static IReadOnlyList<McpContent> ExecuteToolMulti(string name, JsonElement args)
    {
        if (name == "view" && args.ValueKind == JsonValueKind.Object
            && args.TryGetProperty("mode", out var m) && m.ValueKind == JsonValueKind.String)
        {
            var mode = m.GetString() ?? "";
            if (mode is "screenshot" or "p")
                return RunScreenshot(args);
        }
        return new[] { new McpContent("text", Text: ExecuteTool(name, args)) };
    }

    /// <summary>
    /// Render the document as HTML, headless-screenshot to PNG, return both a
    /// text caption (with the saved tmp PNG path, for agents with fs access)
    /// and the base64 PNG (for MCP-only agents). Mirrors the CLI's
    /// <c>view &lt;file&gt; screenshot</c> path; same backend probing
    /// (playwright → chrome → firefox) via <see cref="HtmlScreenshot"/>.
    /// </summary>
    private static IReadOnlyList<McpContent> RunScreenshot(JsonElement args)
    {
        string Arg(string key) => args.TryGetProperty(key, out var v) ? v.GetString() ?? "" : "";
        int? ArgIntOpt(string key) => args.TryGetProperty(key, out var v) && v.TryGetInt32(out var i) ? i : null;
        int ArgInt(string key, int def) => ArgIntOpt(key) ?? def;

        var file = Arg("file");
        if (string.IsNullOrEmpty(file)) throw new ArgumentException("file= required for screenshot");
        var start = ArgIntOpt("start");
        var end = ArgIntOpt("end");
        var width = ArgInt("screenshot_width", 1600);
        var height = ArgInt("screenshot_height", 1200);
        var grid = ArgInt("grid", 0);
        var renderMode = (Arg("render") is { Length: > 0 } rm ? rm : "auto").ToLowerInvariant();
        if (renderMode is not ("auto" or "native" or "html"))
            throw new ArgumentException($"Invalid render value: {renderMode}. Valid: auto, native, html");

        using var handler = DocumentHandlerFactory.Open(file);
        string? html = null;
        byte[]? directPng = null;
        if (handler is Handlers.PowerPointHandler ppt)
        {
            var pStart = start ?? 1;
            var pEnd = end ?? pStart;
            html = ppt.ViewAsHtml(pStart, pEnd, grid, width);
        }
        else if (handler is Handlers.ExcelHandler ex) html = ex.ViewAsHtml();
        else if (handler is Handlers.WordHandler wh)
        {
            // CONSISTENCY(screenshot-default-first-page): mirror CLI — screenshot
            // mode defaults to page 1 for docx so multi-page docs aren't silently
            // cropped by the viewport. Caller can pass start=N to override.
            var pageFilter = (start ?? 1).ToString();
            if (end is int e && e >= (start ?? 1)) pageFilter = $"{start ?? 1}-{e}";
            if (renderMode != "html" && OperatingSystem.IsWindows())
            {
                try { directPng = OfficeCli.Core.WordPdfBackend.Render(file, pageFilter); } catch { directPng = null; }
            }
            if (renderMode == "native" && directPng == null)
                throw new ArgumentException("render=native requires Windows with Microsoft Word installed.");
            if (directPng == null) html = wh.ViewAsHtml(pageFilter);
        }

        if (html == null && directPng == null)
            throw new ArgumentException("Screenshot mode is only supported for .pptx, .xlsx, and .docx files.");

        var stem = Path.GetFileNameWithoutExtension(file);
        var pngPath = Path.Combine(Path.GetTempPath(), $"officecli_screenshot_{stem}_{Guid.NewGuid():N}.png");
        string backendName;
        if (directPng != null)
        {
            File.WriteAllBytes(pngPath, directPng);
            backendName = "word";
        }
        else
        {
            var tmpHtml = Path.Combine(Path.GetTempPath(), $"officecli_preview_{stem}_{Guid.NewGuid():N}.html");
            File.WriteAllText(tmpHtml, html!);
            var r = OfficeCli.Core.HtmlScreenshot.Capture(tmpHtml, pngPath, width, height);
            try { File.Delete(tmpHtml); } catch { /* ignore */ }
            if (!r.Ok)
                throw new InvalidOperationException(
                    "No headless browser available. Install Chrome/Edge/Chromium or Firefox, "
                    + "or `pip install playwright && playwright install chromium`."
                    + (r.Error != null ? $" Last error: {r.Error}" : ""));
            backendName = r.Backend;
        }

        var bytes = File.ReadAllBytes(pngPath);
        var b64 = Convert.ToBase64String(bytes);
        string pagesNote = "";
        if (handler is Handlers.PowerPointHandler pptp)
            pagesNote = $" Slides: {pptp.GetSlideCount()}.";
        var caption = $"Screenshot saved to {pngPath} ({bytes.Length} bytes, backend: {backendName}).{pagesNote}";
=======
    // ==================== Thin command-line exec ====================
    // The MCP tool is a thin shell over the CLI: the caller passes the officecli
    // command line (a string, or a pre-split argv array) and it runs through the
    // SAME System.CommandLine root the CLI uses. No per-command marshalling here
    // means no argument can be silently dropped (every CLI flag works for free),
    // and the model writes exactly what the skills' CLI examples show.

    private static (IReadOnlyList<McpContent> Contents, bool IsError) ExecuteCommandLine(JsonElement args)
    {
        var argv = ExtractArgv(args);
        if (argv.Length == 0)
            throw new ArgumentException("Provide the officecli command line as `command`, e.g. "
                + "command=\"help\" or command=\"add deck.pptx /slide[1] --type shape --prop text=Hi\".");
        // load_skill / skills live in Program.cs early-dispatch, not in the
        // System.CommandLine root, so RunCliRaw can't reach them. Serve them
        // here from the same SkillInstaller the CLI uses.
        if (argv[0] is "load_skill" or "skill" or "skills")
            return (new[] { new McpContent("text", Text: HandleSkillCommand(argv)) }, false);
        if (IsScreenshot(argv))
            return (RunScreenshotArgv(argv), false);
        return SurfaceCliResult(RunCliRaw(argv));
    }

    private static string[] ExtractArgv(JsonElement args)
    {
        if (args.ValueKind != JsonValueKind.Object || !args.TryGetProperty("command", out var c))
            return Array.Empty<string>();
        string[] argv;
        if (c.ValueKind == JsonValueKind.Array)
            // Preserve empty-string elements: the array form is exactly how a
            // caller delivers an intentionally-empty argument value (e.g.
            // `--prop text=` to clear text), so dropping "" would silently
            // diverge from the equivalent quoted "" in the string form. A
            // non-string element (a bare number/bool) is rendered to its JSON
            // text rather than throwing.
            argv = c.EnumerateArray()
                    .Select(e => e.ValueKind == JsonValueKind.String ? (e.GetString() ?? "") : e.GetRawText())
                    .ToArray();
        else if (c.ValueKind == JsonValueKind.String)
            argv = Tokenize(c.GetString() ?? "");
        else
            // A non-string, non-array `command` (number, bool, object, null) is a
            // client mistake — fall through to the empty-argv friendly guidance
            // rather than letting JsonElement.GetString() throw a raw .NET message.
            return Array.Empty<string>();
        // A model copying a skill example may include the leading binary name.
        if (argv.Length > 0 && (argv[0] == "officecli" || argv[0] == "officecli.exe"
            || argv[0].EndsWith("/officecli", StringComparison.Ordinal)))
            argv = argv[1..];
        return argv;
    }

    // Quote-aware tokenizer: splits on whitespace, honours single/double quotes
    // and backslash escapes inside double quotes. Never invokes a shell, so there
    // is no command-injection surface — tokens go straight to the in-process
    // System.CommandLine parser.
    private static string[] Tokenize(string s)
    {
        var tokens = new List<string>();
        var sb = new StringBuilder();
        bool inTok = false; char quote = '\0';
        for (int i = 0; i < s.Length; i++)
        {
            char ch = s[i];
            if (quote != '\0')
            {
                if (ch == quote) quote = '\0';
                // Inside double quotes a backslash only escapes the two chars
                // that would otherwise affect quoting itself (" and \), matching
                // bash double-quote semantics. ANY other backslash sequence is
                // preserved verbatim — crucially `\n` / `\t` stay two characters
                // so the downstream prop parser can turn them into a newline/tab.
                // (The old "escape the next char" rule swallowed the backslash,
                // turning text="A\nB" into the literal "AnB".)
                else if (ch == '\\' && quote == '"' && i + 1 < s.Length && (s[i + 1] == '"' || s[i + 1] == '\\'))
                    sb.Append(s[++i]);
                else sb.Append(ch);
                inTok = true;
            }
            else if (ch == '"' || ch == '\'') { quote = ch; inTok = true; }
            else if (char.IsWhiteSpace(ch)) { if (inTok) { tokens.Add(sb.ToString()); sb.Clear(); inTok = false; } }
            else { sb.Append(ch); inTok = true; }
        }
        if (inTok) tokens.Add(sb.ToString());
        return tokens.ToArray();
    }

    private static bool IsScreenshot(string[] argv)
        => argv.Length >= 2 && argv[0] == "view" && Array.IndexOf(argv, "screenshot") >= 0;

    // Mirror the CLI's load_skill early-dispatch (Program.cs): no name → catalog;
    // a name → that skill's SKILL.md; name + --path <rel> → one reference file.
    private static string HandleSkillCommand(string[] argv)
    {
        string? name = null, relPath = null;
        for (int i = 1; i < argv.Length; i++)
        {
            var a = argv[i];
            if (a == "--path" && i + 1 < argv.Length) { relPath = argv[++i]; continue; }
            if (a == "list") continue;   // `skills list`
            name ??= a;
        }
        if (string.IsNullOrEmpty(name))
            return OfficeCli.Core.SkillInstaller.BuildSkillCatalog();
        return string.IsNullOrEmpty(relPath)
            ? OfficeCli.Core.SkillInstaller.LoadSkillContent(name)
            : OfficeCli.Core.SkillInstaller.LoadSkillFile(name, relPath);
    }

    // screenshot delegates to the CLI (view <file> screenshot ... -o <tmp>) and
    // returns the rendered PNG inline as an image content block. Injects an -o
    // path when the caller didn't give one so we know which file to read back.
    private static IReadOnlyList<McpContent> RunScreenshotArgv(string[] argv)
    {
        var list = argv.ToList();
        int oi = list.FindIndex(a => a == "-o" || a == "--out");
        string outPath;
        string? autoTemp = null;
        if (oi >= 0 && oi + 1 < list.Count) outPath = list[oi + 1];
        else { outPath = Path.Combine(Path.GetTempPath(), $"officecli_mcp_shot_{Guid.NewGuid():N}.png"); autoTemp = outPath; list.Add("-o"); list.Add(outPath); }
        var r = RunCliRaw(list.ToArray());
        if (r.Exit != 0)
            throw new ArgumentException(StripErrPrefix(FirstNonEmpty(r.Stderr.Trim(), r.Stdout.Trim())));
        if (!File.Exists(outPath))
        {
            var m = System.Text.RegularExpressions.Regex.Match(r.Stdout, @"(\S+\.png)");
            if (m.Success && File.Exists(m.Groups[1].Value)) outPath = m.Groups[1].Value;
        }
        if (!File.Exists(outPath))
            return new[] { new McpContent("text", Text: r.Stdout.Trim().Length > 0 ? r.Stdout.Trim() : "Screenshot produced no image file.") };
        var b64 = Convert.ToBase64String(File.ReadAllBytes(outPath));
        // The PNG is returned inline as base64; an auto-injected temp file has no
        // further use, so don't leave it accumulating in the system temp dir. A
        // caller-supplied -o is theirs to keep.
        var caption = $"Screenshot saved to {outPath}";
        if (autoTemp != null && outPath == autoTemp)
        {
            try { File.Delete(autoTemp); } catch { /* best effort — inline data already captured */ }
            caption = "Screenshot rendered (returned inline).";
        }
>>>>>>> upstream/main
        return new[]
        {
            new McpContent("text", Text: caption),
            new McpContent("image", Data: b64, MimeType: "image/png"),
        };
    }

<<<<<<< HEAD
    private static string StatsWithOptionalPageCount(IDocumentHandler handler, JsonElement args, string file)
    {
        var stats = handler.ViewAsStats();
        var wantPages = args.ValueKind == JsonValueKind.Object
            && args.TryGetProperty("page_count", out var pcv)
            && (pcv.ValueKind == JsonValueKind.True || (pcv.ValueKind == JsonValueKind.String && pcv.GetString() == "true"));
        if (!wantPages || handler is not Handlers.WordHandler wh) return stats;
        int? pages = null;
        if (OperatingSystem.IsWindows())
        {
            try { pages = Core.WordPdfBackend.GetPageCount(file); } catch { pages = null; }
        }
        if (pages == null)
        {
            var tmpHtml = Path.Combine(Path.GetTempPath(), $"officecli_pc_{Path.GetFileNameWithoutExtension(file)}_{Guid.NewGuid():N}.html");
            try
            {
                File.WriteAllText(tmpHtml, wh.ViewAsHtml(null));
                pages = Core.HtmlScreenshot.GetPageCountFromDom(tmpHtml);
            }
            finally { try { File.Delete(tmpHtml); } catch { } }
        }
        return pages.HasValue ? $"Pages: {pages}\n" + stats : stats;
    }

    private static string ExecuteTool(string name, JsonElement args)
    {
        string Arg(string key) => args.ValueKind == JsonValueKind.Object && args.TryGetProperty(key, out var v) ? v.GetString() ?? "" : "";
        int ArgInt(string key, int def) => args.ValueKind == JsonValueKind.Object && args.TryGetProperty(key, out var v) && v.TryGetInt32(out var i) ? i : def;
        int? ArgIntOpt(string key) => args.ValueKind == JsonValueKind.Object && args.TryGetProperty(key, out var v) && v.TryGetInt32(out var i) ? i : null;
        string[] ArgStringArray(string key)
        {
            if (args.ValueKind != JsonValueKind.Object || !args.TryGetProperty(key, out var v) || v.ValueKind != JsonValueKind.Array) return [];
            return v.EnumerateArray().Select(e => e.GetString() ?? "").ToArray();
        }

        switch (name)
        {
            case "create":
            {
                var file = Arg("file");
                BlankDocCreator.Create(file);
                return $"Created {file}";
            }
            case "view":
            {
                var file = Arg("file");
                var mode = Arg("mode");
                var start = ArgIntOpt("start");
                var end = ArgIntOpt("end");
                var maxLines = ArgIntOpt("max_lines");
                using var handler = DocumentHandlerFactory.Open(file);
                if (mode is "html" or "h")
                {
                    if (handler is Handlers.PowerPointHandler pptH)
                        return pptH.ViewAsHtml(start, end);
                    if (handler is Handlers.ExcelHandler excelH)
                        return excelH.ViewAsHtml();
                    if (handler is Handlers.WordHandler wordH)
                        return wordH.ViewAsHtml();
                }
                if (mode is "svg" or "g" && handler is Handlers.PowerPointHandler pptSvg)
                    return pptSvg.ViewAsSvg(start ?? 1);
                return mode.ToLowerInvariant() switch
                {
                    "text" or "t" => handler.ViewAsText(start, end, maxLines, null),
                    "annotated" or "a" => handler.ViewAsAnnotated(start, end, maxLines, null),
                    "outline" or "o" => handler.ViewAsOutline(),
                    "stats" or "s" => StatsWithOptionalPageCount(handler, args, file),
                    "issues" or "i" => OutputFormatter.FormatIssues(handler.ViewAsIssues(null, null), OutputFormat.Json),
                    "forms" or "f" => handler is Handlers.WordHandler wfh
                        ? wfh.ViewAsFormsJson().ToJsonString(OutputFormatter.PublicJsonOptions)
                        : throw new ArgumentException("Forms view is only supported for .docx files."),
                    _ => throw new ArgumentException($"Unknown mode: {mode}")
                };
            }
            case "get":
            {
                var file = Arg("file");
                var path = Arg("path"); if (string.IsNullOrEmpty(path)) path = "/";
                var depth = ArgInt("depth", 1);
                using var handler = DocumentHandlerFactory.Open(file);
                var node = handler.Get(path, depth);
                // Unified envelope: single-path get returns the same
                // {matches, results: [...]} shape as query / get selected.
                return OutputFormatter.FormatNodes(new List<DocumentNode> { node }, OutputFormat.Json);
            }
            case "query":
            {
                var file = Arg("file");
                var selector = Arg("selector");
                var textFilter = Arg("text");
                using var handler = DocumentHandlerFactory.Open(file);
                Func<string, string>? keyResolver =
                    handler is OfficeCli.Handlers.ExcelHandler
                    && OfficeCli.Handlers.ExcelHandler.SelectorTargetsCells(selector)
                        ? OfficeCli.Handlers.ExcelHandler.ResolveCellAttributeAlias : null;
                var (results, _) = AttributeFilter.FilterSelector(selector, handler.Query, keyResolver);
                if (!string.IsNullOrEmpty(textFilter))
                    results = results.Where(n => n.Text != null && n.Text.Contains(textFilter, StringComparison.OrdinalIgnoreCase)).ToList();
                return OutputFormatter.FormatNodes(results, OutputFormat.Json);
            }
            case "set":
            {
                var file = Arg("file");
                var path = Arg("path");
                var props = ParseProps(ArgStringArray("props"));
                OfficeCli.Core.MutationSelectorGuard.EnsureScoped(path, "set");
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                var unsupported = handler.Set(path, props);
                var applied = props.Where(kv => !unsupported.Contains(kv.Key)).ToList();
                var msg = applied.Count > 0
                    ? $"Updated {path}: {string.Join(", ", applied.Select(kv => $"{kv.Key}={kv.Value}"))}"
                    : $"No properties applied to {path}";
                if (unsupported.Count > 0)
                    msg += $"\nUnsupported: {string.Join(", ", unsupported)}";
                return msg;
            }
            case "add":
            {
                var file = Arg("file");
                var parent = Arg("parent");
                var type = Arg("type");
                var index = ArgIntOpt("index");
                var after = Arg("after"); if (string.IsNullOrEmpty(after)) after = null;
                var before = Arg("before"); if (string.IsNullOrEmpty(before)) before = null;
                var position = index.HasValue ? InsertPosition.AtIndex(index.Value)
                    : after != null ? InsertPosition.AfterElement(after)
                    : before != null ? InsertPosition.BeforeElement(before)
                    : null;
                var props = ParseProps(ArgStringArray("props"));
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                var resultPath = handler.Add(parent, type, position, props);
                return $"Added {type} at {resultPath}";
            }
            case "remove":
            {
                var file = Arg("file");
                var path = Arg("path");
                OfficeCli.Core.MutationSelectorGuard.EnsureScoped(path, "remove");
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                handler.Remove(path);
                return $"Removed {path}";
            }
            case "move":
            {
                var file = Arg("file");
                var path = Arg("path");
                var to = Arg("to"); if (string.IsNullOrEmpty(to)) to = null;
                var index = ArgIntOpt("index");
                var mvAfter = Arg("after"); if (string.IsNullOrEmpty(mvAfter)) mvAfter = null;
                var mvBefore = Arg("before"); if (string.IsNullOrEmpty(mvBefore)) mvBefore = null;
                var mvPosition = index.HasValue ? InsertPosition.AtIndex(index.Value)
                    : mvAfter != null ? InsertPosition.AfterElement(mvAfter)
                    : mvBefore != null ? InsertPosition.BeforeElement(mvBefore)
                    : null;
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                var resultPath = handler.Move(path, to, mvPosition);
                return $"Moved to {resultPath}";
            }
            case "validate":
            {
                var file = Arg("file");
                using var handler = DocumentHandlerFactory.Open(file);
                var errors = handler.Validate();
                if (errors.Count == 0) return "Validation passed: no errors found.";
                var lines = errors.Select(e => $"[{e.ErrorType}] {e.Description}" +
                    (e.Path != null ? $" (Path: {e.Path})" : ""));
                return $"Found {errors.Count} error(s):\n{string.Join("\n", lines)}";
            }
            case "batch":
            {
                var file = Arg("file");
                var commands = Arg("commands");
                var forceStr = Arg("force");
                var stopOnError = !string.Equals(forceStr, "true", StringComparison.OrdinalIgnoreCase);
                var items = JsonSerializer.Deserialize<List<BatchItem>>(commands, BatchJsonContext.Default.ListBatchItem);
                if (items == null || items.Count == 0)
                    throw new ArgumentException("No commands found in input.");
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                var results = new List<BatchResult>();
                for (int bi = 0; bi < items.Count; bi++)
                {
                    var item = items[bi];
                    try
                    {
                        var output = CommandBuilder.ExecuteBatchItem(handler, item, true);
                        results.Add(new BatchResult { Index = bi, Success = true, Output = output });
                    }
                    catch (Exception ex)
                    {
                        results.Add(new BatchResult { Index = bi, Success = false, Item = item, Error = ex.Message });
                        if (stopOnError) break;
                    }
                }
                var sw = new System.IO.StringWriter();
                CommandBuilder.PrintBatchResults(results, json: true, totalCount: items.Count, output: sw);
                return sw.ToString().Trim();
            }
            case "swap":
            {
                var file = Arg("file");
                var path = Arg("path");
                var path2 = Arg("path2");
                using var handler = DocumentHandlerFactory.Open(file, editable: true);
                var (p1, p2) = handler switch
                {
                    Handlers.PowerPointHandler ppt => ppt.Swap(path, path2),
                    Handlers.WordHandler word => word.Swap(path, path2),
                    Handlers.ExcelHandler excel => excel.Swap(path, path2),
                    _ => throw new InvalidOperationException("swap not supported for this document type")
                };
                return $"Swapped {p1} <-> {p2}";
            }
            case "raw":
            {
                var file = Arg("file");
                var part = Arg("part"); if (string.IsNullOrEmpty(part)) part = "/document";
                using var handler = DocumentHandlerFactory.Open(file);
                return handler.Raw(part, null, null, null);
            }
            case "help":
            {
                // Schema-driven help — single source of truth shared with the CLI's
                // `officecli help` command. The previous implementation was ~150 lines
                // of hardcoded markdown cheat sheets that drifted from schemas/help/*.json
                // (e.g. when chart aliases were added, this block was never updated).
                //
                // Shape (mirrors `officecli help <format> [<element>]`):
                //   {command:"help"}                          → list formats
                //   {command:"help", format:"docx"}           → list elements in that format
                //   {command:"help", format:"docx", type:"paragraph"} → full element schema
                //
                // The Strategy preamble is MCP-specific guidance that schemas don't (and
                // shouldn't) encode — kept inline as McpHelpStrategy.
                var format = Arg("format").ToLowerInvariant();
                var element = Arg("type"); // optional element to drill into

                if (string.IsNullOrEmpty(format))
                    return McpHelpStrategy
                        + "Supported formats: docx, xlsx, pptx.\n"
                        + "Call again with format=<docx|xlsx|pptx> to list elements; "
                        + "add type=<element> for full schema (properties, aliases, examples).";

                if (!OfficeCli.Help.SchemaHelpLoader.IsKnownFormat(format))
                {
                    // CONSISTENCY(mcp-error): truncate user-supplied value in error messages to prevent
                    // response amplification (caller echoes arbitrary-length input back unchanged).
                    var displayFormat = OfficeCli.Help.SchemaHelpLoader.TruncateForError(format, 64);
                    return $"Unknown format '{displayFormat}'. Supported: docx, xlsx, pptx.";
                }

                var canonical = OfficeCli.Help.SchemaHelpLoader.NormalizeFormat(format);
                var sb = new StringBuilder(McpHelpStrategy);

                if (string.IsNullOrEmpty(element))
                {
                    sb.Append("# ").Append(canonical.ToUpperInvariant()).AppendLine(" Elements");
                    sb.AppendLine();
                    foreach (var el in OfficeCli.Help.SchemaHelpLoader.ListElements(canonical))
                        sb.Append("- ").AppendLine(el);
                    sb.AppendLine();
                    var sampleElement = canonical switch { "docx" => "paragraph", "xlsx" => "cell", _ => "shape" };
                    sb.Append("Call again with type=<element> for the full schema. ");
                    sb.Append("Example: {\"command\":\"help\",\"format\":\"").Append(canonical)
                      .Append("\",\"type\":\"").Append(sampleElement).AppendLine("\"}");
                    return sb.ToString();
                }

                try
                {
                    using var doc = OfficeCli.Help.SchemaHelpLoader.LoadSchema(canonical, element);
                    sb.Append(OfficeCli.Help.SchemaHelpRenderer.RenderHuman(doc, null));
                    return sb.ToString();
                }
                catch (Exception ex)
                {
                    return $"{ex.Message}\n\nList available elements via: {{\"command\":\"help\",\"format\":\"{canonical}\"}}";
                }
            }
            case "load_skill":
            {
                // Return the embedded SKILL.md content for the named skill. Pure
                // read — no install side-effect. Identical semantics to the CLI
                // `officecli load_skill <name>` command (both share LoadSkillContent).
                // Agents that want disk-resident skills run `officecli skills install`
                // themselves.
                var skill = Arg("name");
                if (string.IsNullOrEmpty(skill))
                    throw new ArgumentException($"name= required. Available: {OfficeCli.Core.SkillInstaller.KnownSkillsList()}");
                try { return OfficeCli.Core.SkillInstaller.LoadSkillContent(skill); }
                catch (ArgumentException ex)
                {
                    // CONSISTENCY(mcp-error): error message already includes the
                    // truncated input via SkillInstaller; re-throw as-is so MCP
                    // returns a structured error to the caller.
                    throw new ArgumentException(ex.Message);
                }
            }
            default:
                // CONSISTENCY(mcp-error): truncate caller-supplied value to prevent
                // response amplification (echo arbitrary-length input back unchanged).
                throw new ArgumentException($"Unknown tool: {OfficeCli.Help.SchemaHelpLoader.TruncateForError(name, 64)}");
        }
    }

    private static Dictionary<string, string> ParseProps(string[] propStrs)
    {
        var props = new Dictionary<string, string>();
        foreach (var p in propStrs)
        {
            var eq = p.IndexOf('=');
            if (eq > 0) props[p[..eq]] = p[(eq + 1)..];
        }
        return props;
    }

=======
    // ====================================================================
    // Shared-grammar dispatch (Phase 1 of routing MCP through the CLI's one
    // System.CommandLine root). Translating the MCP JSON into the CLI token
    // vector and parsing it with the SAME root the CLI uses means argument
    // validation, business logic, and the {success,data} envelope are shared
    // by construction — not re-marshalled (and re-bugged) by hand here.
    // ====================================================================
    private static RootCommand? _rootCommand;
    private static RootCommand RootCommand => _rootCommand ??= CommandBuilder.BuildRootCommand();

    private readonly record struct CliResult(int Exit, string Stdout, string Stderr);

    /// <summary>
    /// Parse+invoke argv through the shared CLI root, capturing stdout AND
    /// stderr and the exit code. argv is the CLI token vector, e.g.
    /// ["get", file, "/body", "--depth", "1", "--json"].
    ///
    /// Parse/validation failures are NOT short-circuited here. Letting Invoke
    /// run renders the SAME error + usage block a terminal user sees
    /// (System.CommandLine writes it to the captured stream and returns a
    /// non-zero exit WITHOUT running the handler), so the agent receives the
    /// full message — including the option list that points it at the right
    /// flag (e.g. batch's --commands/--input) — instead of a terse, usage-
    /// stripped one-liner. Surfacing only `pr.Errors` here used to drop that
    /// usage block, making MCP less informative than the bare CLI.
    /// </summary>
    private static CliResult RunCliRaw(string[] argv)
    {
        var pr = RootCommand.Parse(argv);
        var prevOut = Console.Out;
        var prevErr = Console.Error;
        var so = new System.IO.StringWriter();
        var se = new System.IO.StringWriter();
        int exit;
        try { Console.SetOut(so); Console.SetError(se); exit = pr.Invoke(); }
        finally { Console.SetOut(prevOut); Console.SetError(prevErr); }
        return new CliResult(exit, so.ToString(), se.ToString());
    }

    // Translate a CLI invocation's (exit, stdout, stderr) into MCP content.
    //
    // Always surface stdout AND stderr together when both are present, so the
    // caller never loses context — neither the "Added/Updated …" success line nor
    // an advisory caveat. A dangling-style add/set exits 0 with the warning on
    // stderr; both now report success WITH the warning visible (the warning was
    // previously dropped on the exit-0 path).
    //
    // Only a genuine failure raises: exit 1 (e.g. path not found, nothing applied),
    // or exit 2 with no stdout (goto/mark emit a usage error to stderr and write
    // no success line). An exit-2 add/set with a populated stdout is the CLI's
    // "applied with caveats" path — the element was added (envelope success:true)
    // and only an unsupported property was dropped; surfacing that as a hard error
    // makes agents re-issue an op that already landed. Scripts still see exit 2
    // from the CLI itself — fail-fast is preserved there, not on the MCP surface.
    private static (IReadOnlyList<McpContent> Contents, bool IsError) SurfaceCliResult(CliResult r)
    {
        var stdout = r.Stdout.TrimEnd('\n', '\r');
        var stderr = r.Stderr.Trim();
        var combined = stdout.Length > 0 && stderr.Length > 0 ? $"{stdout}\n{stderr}"
                     : stdout.Length > 0 ? stdout : stderr;
        // exit 2 with stdout = "applied with caveats" (element added, only an
        // unsupported property dropped) — the op landed, so it is NOT an error.
        // Exit 2 covers two verdicts: "applied with caveats" (envelope
        // success:true, e.g. one unsupported prop dropped) AND "nothing
        // applied" (success:false, every prop refused). Reading the exit code
        // alone reported the second as not-an-error, so an agent whose edit
        // never landed was told it had. The envelope is the business verdict —
        // when stdout carries one, it decides; text mode falls back to the
        // "Error:" prefix the CLI puts on a refused command.
        bool appliedWithCaveats = r.Exit == 2 && stdout.Length > 0
            && (EnvelopeSuccess(stdout) ?? !stdout.TrimStart().StartsWith("Error", StringComparison.OrdinalIgnoreCase));
        bool isError = r.Exit != 0 && !appliedWithCaveats;
        // Surface the CLI output VERBATIM — exit mirrors envelope.success, so a
        // non-zero *business* verdict (batch with a failed step, validate
        // failure) still wrote its {success:false} envelope to stdout; prefixing
        // or munging it would break JSON parsing. A genuine process error has no
        // stdout and its handler-written stderr already carries its own "Error: "
        // prefix, so it too is surfaced as-is (no doubled prefix). The pass/fail
        // bit rides on isError, not on the text — exactly like a terminal user
        // reading stdout plus the exit code.
        var text = combined.Length == 0 ? (isError ? "Command failed." : "(ok)") : combined;
        return (new[] { new McpContent("text", Text: text) }, isError);
    }

    /// <summary>The envelope's top-level `success`, or null when stdout is not a JSON object.</summary>
    private static bool? EnvelopeSuccess(string stdout)
    {
        var t = stdout.TrimStart();
        if (!t.StartsWith('{')) return null;
        try
        {
            using var doc = System.Text.Json.JsonDocument.Parse(t);
            return doc.RootElement.TryGetProperty("success", out var v) && v.ValueKind == System.Text.Json.JsonValueKind.False ? false
                 : doc.RootElement.TryGetProperty("success", out v) && v.ValueKind == System.Text.Json.JsonValueKind.True ? true
                 : null;
        }
        catch (System.Text.Json.JsonException) { return null; }
    }

    private static string FirstNonEmpty(params string[] xs) =>
        xs.FirstOrDefault(x => !string.IsNullOrWhiteSpace(x)) ?? "Command failed.";

    // The MCP catch block prepends "Error: "; the text-mode handlers already
    // wrote "Error: ..." to stderr. Strip one leading prefix to avoid doubling.
    private static string StripErrPrefix(string s) =>
        s.StartsWith("Error: ", StringComparison.Ordinal) ? s["Error: ".Length..] : s;

>>>>>>> upstream/main
    // ==================== Tool Definitions ====================

    // MCP-specific guidance prepended to every help response. Cannot be derived
    // from schemas/help/*.json — it's about how to use the *tool*, not what the
    // *document model* exposes.
    private const string McpHelpStrategy = @"## Strategy
Use view (outline/stats/issues/annotated) to understand the document first, then get/query to inspect details, then set/add/remove to modify.
<<<<<<< HEAD
View modes: text, annotated, outline, stats, issues, html, svg (pptx only), forms (docx only).
=======
View modes: text, annotated, outline, stats, issues, html, svg (pptx only), screenshot, forms (docx only).
Before delivering, pass the delivery gate (see the tool description): validate clean, view issues clean, then a visual audit via view mode=screenshot when layout matters (slide decks most of all). Whether the visual audit is mandatory is format-specific — run `load_skill <pptx|word|excel>` for the authoritative per-format gate.
>>>>>>> upstream/main
For 3+ mutations on the same file, use batch (one open/save cycle) instead of separate calls.
Get output keys can be used directly as Set input keys (round-trip safe).
Colors: FF0000, red, rgb(255,0,0), accent1. Sizes: 24pt. Positions: 2cm, 1in, 72pt, or raw EMU.
Paths are 1-based: /slide[1]/shape[2], /body/p[3], /Sheet1/A1.

";

<<<<<<< HEAD
    private const string ToolDescription = @"Create, read, and modify Office documents (.docx, .xlsx, .pptx).

Commands: create (file), view (file, mode: text|annotated|outline|stats|issues|html|svg|screenshot|forms), get (file, path, depth), query (file, selector), set (file, path, props[]), add (file, parent, type, props[], index/after/before), remove (file, path), move (file, path, to, index/after/before), swap (file, path, path2), validate (file), batch (file, commands), raw (file, part), help (format: docx|xlsx|pptx, optional type=<element> for full schema), load_skill (name: pptx|word|excel|morph-ppt|morph-ppt-3d|pitch-deck|academic-paper|data-dashboard|financial-model — returns the skill's SKILL.md guidance).

Paths are 1-based: /slide[1]/shape[2], /body/p[3], /Sheet1/A1. Props are key=value strings. Call help with format= to list elements, then help with format= and type= to drill into a specific element's schema (properties, aliases, examples).";
=======
    private const string ToolDescription = @"Create, read, and modify Office documents (.docx, .xlsx, .pptx) by running officecli command lines.

Pass an officecli command line in `command` (string or pre-split argv array); it runs through the same CLI you'd use in a terminal. Verbs: create, view (modes: text|annotated|outline|stats|issues|html|svg|screenshot|forms), get, query, set, add, remove, move, swap, validate, batch, raw, help, load_skill. Add --json to get/query/validate/view-issues for structured output. Examples (CLI syntax): create deck.pptx · add deck.pptx /slide[1] --type shape --prop ""text=Hi"" · set report.docx /body/p[1] --prop bold=true · view deck.pptx screenshot --page 2 · query book.xlsx ""cell[bold=true]"". Discover verbs/flags with `help`, and an element's schema with `help <format> <element>` (e.g. help pptx shape).

Paths are 1-based: /slide[1]/shape[2], /body/p[3], /Sheet1/A1. Props are key=value strings.

Delivery gate (before reporting a document finished — any failure = fix and re-check, do NOT deliver; validate passing is NOT delivery, 'looks like a real document' is):
1. Schema: `validate <file>` -> clean, no errors.
2. Content: `view <file> issues` -> no overflow/format/structure issues; and scan `view <file> text` for leftover placeholders (xxxx, lorem/ipsum, <TODO>, {{...}}, $VAR$, empty ()/[]).
3. Visual audit: `view <file> screenshot --page N` renders the page/slide and returns it as an image shown to you (or --grid auto for a whole-doc contact sheet). Judge it adversarially (assume problems exist) for overlap, text overflow, off-slide shapes, dark-on-dark, misalignment; fix positions/sizes (`set <file> <path> --prop x=.. --prop y=..`) and re-screenshot until right; if the screenshot can't render, say 'not visually verified'. Whether this audit is mandatory is format-specific (slide decks need it most — absolute-positioned shapes overlap invisibly to text modes), so run `load_skill pptx` (or word / excel) for the authoritative gate. The per-format SKILL.md, not this blurb, is the source of truth for what 'done' requires.
4. Flush to disk: end with `save <file>` — this guarantees your edits are written to disk before you hand the file off. Required final step, not optional (always safe — never errors or loses work; `close` also flushes if you want to end the session too).";
>>>>>>> upstream/main

    private static void WriteToolDefinitions(Utf8JsonWriter w)
    {
        w.WriteStartObject();
        w.WriteString("name", "officecli");
<<<<<<< HEAD
        w.WriteString("description", ToolDescription);
        w.WriteStartObject("inputSchema");
        w.WriteString("type", "object");
        w.WriteStartObject("properties");
        // command
        w.WriteStartObject("command"); w.WriteString("type", "string");
        w.WriteStartArray("enum");
        foreach (var c in new[] { "create", "view", "get", "query", "set", "add", "remove", "move", "swap", "validate", "batch", "raw", "help", "load_skill" })
            w.WriteStringValue(c);
        w.WriteEndArray();
        w.WriteString("description", "Command to execute");
        w.WriteEndObject();
        // file
        w.WriteStartObject("file"); w.WriteString("type", "string"); w.WriteString("description", "Document file path"); w.WriteEndObject();
        // path
        w.WriteStartObject("path"); w.WriteString("type", "string"); w.WriteString("description", "DOM path (e.g. /slide[1]/shape[1], /Sheet1/A1, /body/p[1])"); w.WriteEndObject();
        // parent
        w.WriteStartObject("parent"); w.WriteString("type", "string"); w.WriteString("description", "Parent DOM path for add"); w.WriteEndObject();
        // type
        w.WriteStartObject("type"); w.WriteString("type", "string"); w.WriteString("description", "Element type for add (slide, shape, paragraph, run, table, picture, chart, etc.)"); w.WriteEndObject();
        // selector
        w.WriteStartObject("selector"); w.WriteString("type", "string"); w.WriteString("description", "CSS-like selector for query. Valid element types per handler: PPT — shape, textbox, title, picture, table, chart, placeholder, connector, group, zoom, ole, equation (NOT 'slide' — use 'slide[N]>shape' to scope); Excel — cell, sheet, row, column, table, chart, image; Word — paragraph, run, table, image, hyperlink, heading, list. Supports attribute filters ('shape[text=Hello]', 'paragraph[style=Normal] > run[font!=Arial]'), pseudo-selectors (:contains(...), :empty), and Excel cell aliases (bold, size → font.bold, font.size). Path-style selectors starting with '/' are rejected except '/slide[N]/...' scoping in PPT."); w.WriteEndObject();
        // text (query post-filter)
        w.WriteStartObject("text"); w.WriteString("type", "string"); w.WriteString("description", "Filter query results to elements whose text contains this substring (case-insensitive)"); w.WriteEndObject();
        // props
        w.WriteStartObject("props"); w.WriteString("type", "array");
        w.WriteStartObject("items"); w.WriteString("type", "string"); w.WriteEndObject();
        w.WriteString("description", "key=value pairs (e.g. bold=true, color=FF0000, text=Hello)"); w.WriteEndObject();
        // mode
        w.WriteStartObject("mode"); w.WriteString("type", "string"); w.WriteString("description", "View mode: text, annotated, outline, stats, issues, html, svg (pptx), screenshot (PNG via headless browser; needs playwright/chrome/firefox; takes seconds), forms (docx)"); w.WriteEndObject();
        // screenshot_width / screenshot_height / grid (screenshot mode)
        w.WriteStartObject("screenshot_width"); w.WriteString("type", "number"); w.WriteString("description", "Viewport width for screenshot mode (default 1600)"); w.WriteEndObject();
        w.WriteStartObject("screenshot_height"); w.WriteString("type", "number"); w.WriteString("description", "Viewport height for screenshot mode (default 1200)"); w.WriteEndObject();
        w.WriteStartObject("grid"); w.WriteString("type", "number"); w.WriteString("description", "Tile slides into N-column thumbnail grid (screenshot mode, pptx only; 0 = off)"); w.WriteEndObject();
        // depth
        w.WriteStartObject("depth"); w.WriteString("type", "number"); w.WriteString("description", "Child depth for get (default 1)"); w.WriteEndObject();
        // index
        w.WriteStartObject("index"); w.WriteString("type", "number"); w.WriteString("description", "Insert position (0-based) for add/move"); w.WriteEndObject();
        // to
        w.WriteStartObject("to"); w.WriteString("type", "string"); w.WriteString("description", "Target parent path for move"); w.WriteEndObject();
        // after, before, path2
        w.WriteStartObject("after"); w.WriteString("type", "string"); w.WriteString("description", "Insert after this sibling path (for add/move)"); w.WriteEndObject();
        w.WriteStartObject("before"); w.WriteString("type", "string"); w.WriteString("description", "Insert before this sibling path (for add/move)"); w.WriteEndObject();
        w.WriteStartObject("path2"); w.WriteString("type", "string"); w.WriteString("description", "Second path for swap"); w.WriteEndObject();
        // start, end, max_lines
        w.WriteStartObject("start"); w.WriteString("type", "number"); w.WriteString("description", "Start line for view"); w.WriteEndObject();
        w.WriteStartObject("end"); w.WriteString("type", "number"); w.WriteString("description", "End line for view"); w.WriteEndObject();
        w.WriteStartObject("max_lines"); w.WriteString("type", "number"); w.WriteString("description", "Max lines for view"); w.WriteEndObject();
        // commands
        w.WriteStartObject("commands"); w.WriteString("type", "string"); w.WriteString("description", "JSON array of batch commands"); w.WriteEndObject();
        // force
        w.WriteStartObject("force"); w.WriteString("type", "string"); w.WriteString("description", "Set to 'true' to continue batch on error (default: stop on first error)"); w.WriteEndObject();
        // part
        w.WriteStartObject("part"); w.WriteString("type", "string"); w.WriteString("description", "Part path for raw (e.g. /document, /styles, /slide[1])"); w.WriteEndObject();
        // format
        w.WriteStartObject("format"); w.WriteString("type", "string"); w.WriteString("description", "Document format for help: xlsx, pptx, docx"); w.WriteEndObject();
        // name (for load_skill)
        w.WriteStartObject("name"); w.WriteString("type", "string"); w.WriteString("description", "Skill name for load_skill: pptx, word, excel, morph-ppt, morph-ppt-3d, pitch-deck, academic-paper, data-dashboard, financial-model"); w.WriteEndObject();
=======
        // Append a compact always-on skill-trigger summary so the agent is
        // prompted to load the right skill without the full ~1.2k of routing
        // descriptions resident in context. Detail stays lazy behind load_skill.
        w.WriteString("description", ToolDescription + "\n\n" + McpHelpStrategy + "\n"
            + OfficeCli.Core.SkillInstaller.BuildSkillTriggerSummary());
        w.WriteStartObject("inputSchema");
        w.WriteString("type", "object");
        w.WriteStartObject("properties");
        // Single param: the officecli command line, as a string or a pre-split
        // argv array. Everything else (verbs, flags, schemas) is discovered via
        // `help` and the loaded skills — no per-command schema to drift.
        w.WriteStartObject("command");
        // A union `type: ["string","array"]` with a sibling `items` is valid
        // JSON Schema, but the Gemini function-calling schema takes a single
        // type and rejects `items` unless that type is ARRAY — every request
        // through a Gemini-backed client failed with HTTP 400 before the model
        // saw a prompt. `anyOf` with one branch per shape is accepted by every
        // client that took the union, and by Gemini.
        w.WriteStartArray("anyOf");
        w.WriteStartObject(); w.WriteString("type", "string"); w.WriteEndObject();
        w.WriteStartObject(); w.WriteString("type", "array");
        w.WriteStartObject("items"); w.WriteString("type", "string"); w.WriteEndObject();
        w.WriteEndObject();
        w.WriteEndArray();
        w.WriteString("description",
            "The officecli command line — either a single string (e.g. \"add deck.pptx /slide[1] --type shape --prop text=Hi\") "
            + "or a pre-split argv array of strings (use the array form when an argument contains spaces or quotes). A leading "
            + "'officecli' is optional. Examples: \"help\" lists commands; \"help pptx shape\" shows an element's schema; "
            + "\"view deck.pptx text\" reads it; \"view deck.pptx screenshot --page 2\" returns a rendered image; add --json to "
            + "get/query/validate for structured output. Run help first to learn the verbs and flags.");
        w.WriteEndObject();
>>>>>>> upstream/main
        w.WriteEndObject(); // end properties
        w.WriteStartArray("required"); w.WriteStringValue("command"); w.WriteEndArray();
        w.WriteEndObject(); // end inputSchema
        w.WriteEndObject(); // end tool
    }

    // ==================== JSON-RPC Helpers ====================

    private static string WriteJson(Action<Utf8JsonWriter> build)
    {
        using var ms = new MemoryStream();
        using (var w = new Utf8JsonWriter(ms)) build(w);
        return Encoding.UTF8.GetString(ms.ToArray());
    }

    private static void Rpc(Utf8JsonWriter w, JsonElement? id)
    {
        w.WriteString("jsonrpc", "2.0");
        if (id.HasValue) { w.WritePropertyName("id"); id.Value.WriteTo(w); }
        else w.WriteNull("id");
    }

    private static string ErrorJson(JsonElement? id, int code, string message) => WriteJson(w =>
    {
        w.WriteStartObject();
        Rpc(w, id);
        w.WriteStartObject("error");
        w.WriteNumber("code", code);
        w.WriteString("message", message);
        w.WriteEndObject();
        w.WriteEndObject();
    });
}
