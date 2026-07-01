# scripts/generate_resources.py ha sido eliminado del proyecto.
# Los tests ya no son aplicables.
# from scripts.generate_resources import domain_from, classify, extract_clean_urls, ENTRIES, CATEGORY_ORDER


# class TestDomainFrom:
#     def test_strips_www(self):
#         assert domain_from("https://www.example.com/page") == "example.com"

#     def test_no_www(self):
#         assert domain_from("https://example.com") == "example.com"

#     def test_subdomain(self):
#         assert domain_from("https://sub.example.com") == "sub.example.com"

#     def test_path_ignored(self):
#         assert domain_from("https://example.com/path/to/page") == "example.com"


# class TestClassify:
#     def test_exact_domain_match(self):
#         result = classify("https://astro.build")
#         assert result is not None
#         assert result["name"] == "Astro"

#     def test_path_specific_before_domain(self):
#         github_gist = classify("https://gist.github.com/user")
#         assert github_gist is not None
#         # gist.github.com should match "gist.github.com" before "github.com"
#         assert github_gist["name"] == "GitHub Gist"

#         # Known path-specific entries
#         zustand = classify("https://github.com/pmndrs/zustand")
#         assert zustand is not None
#         assert zustand["name"] == "Zustand"

#     def test_unknown_domain(self):
#         result = classify("https://this-does-not-exist-12345.com")
#         assert result is None

#     def test_with_www(self):
#         result = classify("https://www.npmjs.com/package/pkg")
#         assert result is not None
#         assert result["name"] == "npm"


# class TestExtractCleanUrls:
#     def test_extracts_urls(self):
#         text = "Visit https://example.com and https://test.org"
#         urls = extract_clean_urls(text)
#         assert "https://example.com" in urls
#         assert "https://test.org" in urls

#     def test_skips_favicon_urls(self):
#         text = 'Check <img src="https://www.google.com/s2/favicons?domain=x" />'
#         urls = extract_clean_urls(text)
#         assert len(urls) == 0

#     def test_deduplicates(self):
#         text = "https://example.com https://example.com"
#         urls = extract_clean_urls(text)
#         assert len(urls) == 1


# class TestCategories:
#     def test_all_entries_have_known_categories(self):
#         known_cats = set(CATEGORY_ORDER)
#         for domain, entry in ENTRIES.items():
#             assert entry["cat"] in known_cats, \
#                 f"Domain '{domain}' has unknown category '{entry['cat']}'"

#     def test_known_categories_have_icon(self):
#         from scripts.generate_resources import CAT_ICON
#         for cat in CATEGORY_ORDER:
#             assert cat in CAT_ICON, f"Category '{cat}' missing icon"

#     def test_all_entries_have_required_fields(self):
#         for domain, entry in ENTRIES.items():
#             assert "name" in entry, f"Domain '{domain}' missing name"
#             assert "cat" in entry, f"Domain '{domain}' missing cat"
#             assert "desc" in entry, f"Domain '{domain}' missing desc"
