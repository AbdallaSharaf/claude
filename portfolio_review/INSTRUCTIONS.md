# Portfolio copy review — instructions for each reviewer

Saber Group is a full-service marketing agency in Tanta, Egypt (strategy, social media
management, photography, video, design, ads). Their website portfolio shows ~143 client
projects. The owner wants every project's text reviewed before anything is edited.
**This is read-only work: do not call any API, do not edit any project. Only read the
chunk file and write your results file.**

Your input file: `chunkN.json` (N given in your task). It is a list of projects. Each has:
`id, slug, published, client, sector, services, tagsEn, tagsAr, cast, texts[]` where each
text is `{field, lang, text}`. Fields: `name`, `description`, `location`,
`sectionK.caption`, `sectionK.description`, `sectionK.text`, `sectionK.before_label/after_label`.

Read EVERY text of EVERY project in your chunk, in both Arabic and English, plus the tags
and the cast titles.

## What to report per project

1. **Suggested names** (`suggested_name_en`, `suggested_name_ar`). Current names are very
   generic ("Desgins", "Jewelry - New year 2026 photoshoot", "Mother's Day Cake
   Photography"). A good name says WHO + WHAT IDEA + WHAT KIND OF WORK, short (max ~60
   chars), e.g. "Zad Jewelry — Red & Gold New Year Campaign". Use only facts present in the
   project's own data (client, texts, captions, services, sector). Never invent results,
   products or claims. Arabic name: natural Modern Standard Arabic suitable for a premium
   agency site, not a word-for-word translation. If the client name is unknown, build the
   name from the concept. Give `name_reason`: one short line on what was wrong with the
   current name (generic / typo / doesn't match content / EN-AR mismatch / fine).
   If the current name is already good, say so and still return it as the suggestion.

2. **Issues** — a list. One entry per concrete problem:
   - `field` (exactly as in the input, e.g. `section2.description`), `lang` (`en`/`ar`)
   - `type`: one of `spelling`, `grammar`, `wording`, `translation_mismatch` (EN and AR say
     different things), `missing_translation` (one language empty or copied in the other
     language), `wrong_language` (Arabic text in the EN field or vice versa), `placeholder`
     (dummy/test/irrelevant text), `inconsistent` (contradicts other fields, e.g. caption says
     video but section has photos, or describes another project), `formatting` (broken
     spacing, stray symbols, all caps, zero-width chars, emoji clutter), `generic` (says
     nothing specific), `claim` (unverifiable superlatives or brand/trademark issues, e.g.
     using a luxury brand name the client is not)
   - `current`: the exact wrong fragment (short excerpt, not the whole paragraph)
   - `suggestion`: the corrected fragment, or for long texts a rewritten version of the
     whole field when the field is weak (keep the facts, improve clarity, same language)
   - `severity`: `high` (visible error a client would notice: typo in a title/caption,
     wrong language, placeholder, missing translation of a name/caption), `medium`
     (description quality, mismatches), `low` (style polish)
   Report every spelling mistake you find; e.g. "Directot", "Jewllery", "desgins",
   Arabic hamza/taa marbuta/alif errors, "لقطات المجهورات". Check cast titles too
   (use field `cast`).

3. **Tag issues** (`tag_issues`): typos, duplicates, irrelevant tags, Arabic tags that are
   not Arabic, EN/AR lists badly out of sync, keyword-stuffing (dozens of near-identical
   tags), missing obvious tags. Give `current` and `suggestion`. Also give
   `suggested_tags_en` and `suggested_tags_ar`: a cleaned list of 8–15 useful tags each.

4. `missing_content`: short list of what the project lacks to show the agency's full
   marketing value (e.g. "no client goal", "no results", "no description for sections",
   "Arabic description missing", "no client name", "no video") — only what is truly missing
   from the data.

5. `quality_score`: 1–5 for how ready the project's text is to publish as-is (5 = ready).

6. `note`: one sentence, anything else the owner should know (or empty).

## Output

Write a single JSON file `resultN.json` in the same folder (same N), an array with one
object per project in your chunk, keys exactly:
`id, current_name_en, current_name_ar, suggested_name_en, suggested_name_ar, name_reason,
issues, tag_issues, suggested_tags_en, suggested_tags_ar, missing_content, quality_score, note`.
Every project in the chunk must appear. Make sure the file is valid JSON (load it with
python to check). Then reply with only: the number of projects reviewed and the total number
of issues found.
