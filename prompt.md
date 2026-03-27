# Effective Prompt for Zhihu Scraper Creation

## Goal
Create a Python script that reliably extracts clean text content from Zhihu (知乎) articles, preserving paragraph structure while handling authentication requirements.

## Key Requirements

### Must-Have Features
- ✅ **HTML Structure Analysis**: Base implementation on the provided HTML example (`ex.html`), specifically targeting:
  ```html
  <div itemprop="text" class="RichText ztext..."><p data-pid="..."></p></div>
  ```
- ✅ **Authentication Support**: Implement cookie-based authentication for login-required content
- ✅ **Error Handling**: Comprehensive error cases (403, content not found, network issues)
- ✅ **User Experience**: Interactive CLI with clear prompts for URL/cookies
- ✅ **Output Quality**: Preserve paragraph structure with `\n\n` separation
- ✅ **Documentation**: Include troubleshooting guide and usage examples

### Technical Constraints
- 🐍 Use Python 3.7+
- 📦 Dependencies limited to `requests` and `beautifulsoup4`
- 🌐 UTF-8 encoding throughout
- 🛑 No headless browsers (avoid Selenium/Playwright)
- 🚫 Never hardcode credentials

## Input Context to Provide
When prompting the AI, include:

1. **Sample HTML**:
   ```
   [Paste relevant snippet from ex.html showing itemprop="text" structure]
   ```

2. **Specific Requirements**:
   - Target element: `itemprop="text"` container
   - Must extract all `<p>` elements within content
   - Cookie format: `key=value` pairs (sessionid, z_c0)

3. **Quality Expectations**:
   - Production-ready error messages
   - First 200 chars preview
   - Saved output to `zhihu_content.txt`

## Prohibited Approaches
- ❌ Guessing CSS selectors without HTML reference
- ❌ Using JavaScript rendering
- ❌ Ignoring authentication requirements
- ❌ Producing unstructured single-paragraph output
- ❌ Omitting ethical considerations

## Expected Output Structure
```python
# Docstring with clear parameters/returns
# Error-specific messages
# Interactive cookie input handler
# UTF-8 file writing
# Troubleshooting tips
```

## Ethical Requirements
⚠️ Must include in documentation:
- Respect for Zhihu's terms of service
- Non-commercial usage disclaimer
- Rate limiting recommendation
- Cookie security warning

## Why This Prompt Works
1. **Precision** - Specifies exact HTML elements to target
2. **Constraint Management** - Prevents common pitfalls (over-engineering, wrong tech)
3. **Quality Gates** - Defines what "done" looks like
4. **Ethical Guardrails** - Builds responsibility into requirements

> 💡 Pro Tip: Always provide the actual HTML sample. AIs fail when asked to "scrape Zhihu" without concrete examples of the target structure.