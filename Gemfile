source "https://rubygems.org"

# Jekyll 主程式
gem "jekyll", "~> 4.3.0"

# GitHub Pages 支援
# gem "github-pages", group: :jekyll_plugins

# Jekyll 插件
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-paginate"
end

# Windows 和 JRuby 不支援 timezone 資料
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# kramdown v2 ships without the gfm parser by default
gem "kramdown-parser-gfm"

# webrick (Ruby 3.0+)
gem "webrick", "~> 1.8"
