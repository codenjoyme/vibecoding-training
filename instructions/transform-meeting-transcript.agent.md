## Purpose

- Transform meeting transcript files (`.docx`) into structured meeting summaries.
- Pipeline: `.docx` → `.txt` (extract text) → `summary-YYYY-MM-DD.md` (structured summary).
- Input: raw transcript file (typically exported from MS Teams or similar).
- Output: `.txt` file (plain text extraction) + `summary-YYYY-MM-DD.md` in the same folder as the source `.docx`.

## File Naming Convention

- The `.txt` file keeps the same base name as the source `.docx` (e.g. `Call about teams.docx` → `Call about teams.txt`).
- Summary file name pattern: `summary-YYYY-MM-DD.md` where the date is taken from the transcript header.
- If the transcript header has no date — use the file's modified date or ask the user.
- For coaching/recurring sessions add session number: `summary-session-N-YYYY-MM-DD.md`.

## Docx to Text Extraction

- Use built-in .NET `System.IO.Compression.FileSystem` — no external libraries needed.
- A `.docx` file is a ZIP archive containing `word/document.xml`.
- Extract text from `<w:t>` elements within `<w:p>` (paragraph) and `<w:r>` (run) elements.
- Convert `<w:br/>` elements to line breaks.
- Each `<w:p>` becomes a separate line.
- PowerShell implementation:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Extract-DocxText {
    param(
        [string]$docxPath,
        [switch]$Anonymize,        # replace speaker name runs with "Speaker N" at parse time
        [string]$MappingPath       # optional: write original->pseudonym map (sensitive, gitignore!)
    )
    $zip = [System.IO.Compression.ZipFile]::OpenRead($docxPath)
    $entry = $zip.GetEntry("word/document.xml")
    $stream = $entry.Open()
    $reader = New-Object System.IO.StreamReader($stream)
    $xmlContent = $reader.ReadToEnd()
    $reader.Close(); $stream.Close(); $zip.Dispose()
    $xml = New-Object System.Xml.XmlDocument
    $xml.PreserveWhitespace = $true     # keep <w:t xml:space="preserve"> spaces
    $xml.LoadXml($xmlContent)
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    $paragraphs = $xml.SelectNodes("//w:p", $ns)
    $map = [ordered]@{}            # original name -> pseudonym (only populated if -Anonymize)
    $lines = @()
    foreach ($p in $paragraphs) {
        $runs = $p.SelectNodes(".//w:r", $ns)
        $lineText = ""
        $lastEmittedName = $null   # collapse consecutive speaker-name runs in the same paragraph
        foreach ($r in $runs) {
            # Speaker-name run = bold + color #616161 + size 24 (Teams transcript convention).
            $rPr = $r.SelectSingleNode("w:rPr", $ns)
            $isSpeakerName = $false
            if ($Anonymize -and $rPr) {
                $b   = $rPr.SelectSingleNode("w:b", $ns)
                $col = $rPr.SelectSingleNode("w:color/@w:val", $ns)
                $sz  = $rPr.SelectSingleNode("w:sz/@w:val", $ns)
                if ($b -and $col -and $col.Value -eq "616161" -and $sz -and $sz.Value -eq "24") {
                    $isSpeakerName = $true
                }
            }
            if ($isSpeakerName) {
                # Collect the run's full name once, emit one pseudonym (do not iterate <w:t> children).
                $name = ($r.SelectNodes(".//w:t", $ns) | ForEach-Object { $_.'#text' }) -join ''
                $name = $name.Trim()
                if ($name -and $name -ne $lastEmittedName) {
                    if (-not $map.Contains($name)) { $map[$name] = "Speaker $($map.Count + 1)" }
                    $lineText += $map[$name] + ' '
                    $lastEmittedName = $name
                }
                continue
            }
            $lastEmittedName = $null   # any non-name run resets the collapse window
            foreach ($child in $r.ChildNodes) {
                if ($child.LocalName -eq "t") { $lineText += $child.'#text' }
                elseif ($child.LocalName -eq "br") { $lineText += "`n" }
            }
        }
        $lines += $lineText
    }
    if ($Anonymize -and $MappingPath) {
        $map | ConvertTo-Json | Set-Content -Path $MappingPath -Encoding UTF8
        Write-Warning "$MappingPath contains real names - gitignore it."
    }
    return ($lines -join "`n")
}
```

- To extract a date from a Teams-style transcript header: parse for pattern `-YYYYMMDD_HHMMSS-` or look at the first lines.

## Participant Anonymization (optional)

- When the meeting is sensitive, replace real names with sequential labels: `Participant A`, `Participant B`, etc.
- Include role in parentheses where known (e.g. `Participant B (Dev)`).
- For internal/technical meetings anonymization is usually NOT required — keep names as-is unless the user asks otherwise.

### Built-in `-Anonymize` switch on `Extract-DocxText`

The PowerShell function above accepts `-Anonymize` (and optional `-MappingPath`). It works **at parse time, not as a post-pass**: while iterating XML runs, any run whose `<w:rPr>` matches the Teams "speaker name" formatting (`<w:b/>` + `<w:color w:val="616161"/>` + `<w:sz w:val="24"/>`) has its text substituted with a sequential pseudonym `Speaker 1`, `Speaker 2`, … *before* it ever lands in the output buffer.

Properties:

- **No regex search for names in the text.** The function never scans the body for known names; the model's output therefore cannot know names that were never written.
- **No code duplication.** There is one parsing loop. `-Anonymize` only changes how a single run is rendered.
- **Optional sidecar** `-MappingPath` writes `original_name → pseudonym` JSON. **This file is sensitive — gitignore it.** It exists only so a human can de-anonymize LLM-returned results.
- **Trade-off:** if a participant is mentioned by name *inside the spoken text* (`"Stiven, can you confirm?"`), the name stays — by design, since we do not search for names in the body. If your transcripts routinely address participants by name, anonymize at the meeting policy level rather than at the parser.

Two trust levels:

- The anonymized output is safe to send to an LLM.
- The mapping JSON must never leave the local machine.

## Generic Meeting Summary Format

Use this structure when the meeting is not part of a recurring series.

```markdown
# Meeting Summary — [Topic]

**Date:** [date from transcript header]  
**Duration:** ~[duration if available]  
**Participants:** [names or anonymized labels]  
**Meeting type:** [discovery / planning / technical / coaching / other]

## Context

- [1–3 bullets describing why the meeting happened and what was on the table]

## Topics Covered

- [List topics discussed; use bold + colon for items that need a short explanation]

## Key Decisions

- [Concrete decisions made during the meeting]

## Action Items

- [Concrete actions, ideally with owner and rough timing]

## Open Questions

- [Things that were raised but not resolved]

## Notes

- [Free-form observations, risks, technical details worth preserving]
```

## Coaching Session Format (Session 1 — Initial Assessment)

Use when the meeting is the first coaching session with a participant.

```markdown
# Session 1 Summary — Participant [X] ([Role])

**Date:** [date from transcript header]  
**Duration:** ~[duration from transcript header]  
**Session type:** Initial assessment + onboarding [+ any additional focus areas]

## Profile

- **Role:** [extracted from conversation]
- **Experience:** [AI/Copilot experience level — concise]
- **IDE:** [which IDE, plugins, configuration]
- **Model:** [which AI model they use or default]
- **Project:** [brief project context]

## Current AI Usage

- [3–6 bullets describing how they currently use AI tools]
- [Include both what they do and what they don't do]

## Key Pain Points Identified

1. **[Pain point name in bold]** — [one sentence description + root cause]
2. ...

## Topics Covered

- [List topics discussed during the session]

## Agreed Next Steps

- [Concrete actions for the participant before next session]

## Coach Notes

- [2–5 candid observations about baseline level, growth areas, PoC potential, risks]
```

## Coaching Session Format (Session 2+ — Follow-up)

Use when prior summaries already exist for this participant.

```markdown
# Session [N] Summary — Participant [X] ([Role])

**Date:** [date from transcript header]  
**Duration:** ~[duration from transcript header]  
**Session type:** Follow-up + [specific focus]

## Progress Since Session [N-1]

- [What the participant did between sessions]
- [Did they complete agreed next steps?]

## Topics Covered

- [Topics discussed in this session]

## Key Pain Points Identified

- [New or reinforced pain points; note which previous ones were resolved]

## Agreed Next Steps

- [Actions for next session]

## Coach Notes

- [Progress assessment, risks, mindset observations]
```

## Extraction Rules

- Extract facts from the conversation — do not invent or assume.
- Transcripts are often noisy (speech-to-text artifacts) — interpret intent, not literal words.
- For pain points: distinguish symptoms from root causes. State both when possible.
- For action items: only include things that were explicitly agreed upon.
- Duration: round to nearest 5 minutes, prefix with `~`.
- When the user asks for a focused summary on a specific subtopic — also produce a dedicated section or a separate file with maximally actionable instructions extracted from the conversation.

## Quality Checklist

- [ ] Date matches the transcript header.
- [ ] All sections are present and filled (or explicitly marked `n/a`).
- [ ] No invented facts — every claim traceable to the transcript.
- [ ] Action items are concrete and actionable.
- [ ] File saved as `summary-YYYY-MM-DD.md` (or `summary-session-N-YYYY-MM-DD.md` for coaching) in the same folder as the transcript.
- [ ] Corresponding `.txt` file exists alongside the `.docx`.
