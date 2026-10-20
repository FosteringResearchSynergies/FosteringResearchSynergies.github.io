// Eleventy 3: sources in src/, output in _site/ (the only thing published, see docs/ROADMAP.md).
//   npm run build               # deletes _site/, then builds it
//   npm run dev -- --port=N     # local preview; a busy port is an error, never a silent switch
import yaml from "js-yaml";

export default function (eleventyConfig) {
    // Data files in YAML (src/_data/*.yml). An empty or comment-only file is null. Unquoted dates
    // become JavaScript dates: the data files quote them ("2026-05-12").
    eleventyConfig.addDataExtension("yml,yaml", (contents) => yaml.load(contents) ?? null);

    // Static files, copied as they are. src/assets/ is served as /assets/; pictures/ and styles.css
    // belong to the pages ported from the old static site and keep their URLs.
    eleventyConfig.addPassthroughCopy("src/assets");
    eleventyConfig.addPassthroughCopy("src/pictures");
    eleventyConfig.addPassthroughCopy("src/styles.css");
    eleventyConfig.addPassthroughCopy("src/events/*.css");

    // Stops the build with a message, for templates that receive invalid arguments:
    // {{ "what went wrong" | fail }}
    eleventyConfig.addFilter("fail", (message) => {
        throw new Error(message);
    });

    // scripts/preview.sh prints the URL before the server starts: the port must be the one asked for.
    eleventyConfig.setServerOptions({ portReassignmentRetryCount: 0 });
}

export const config = {
    dir: {
        input: "src",
        includes: "_includes",
        layouts: "_includes/layouts",
        data: "_data",
        output: "_site",
    },
    templateFormats: ["njk", "md", "html"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
};
