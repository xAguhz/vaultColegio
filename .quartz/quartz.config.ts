import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

// Configuración de la página de vaultColegio (Quartz 4.5.2).
// El workflow .github/workflows/publicar.yml copia este archivo sobre el de Quartz.
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Colegio",
    pageTitleSuffix: " · Colegio",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "es-ES",
    baseUrl: "xaguhz.github.io/vaultColegio",
    ignorePatterns: ["private", ".obsidian", "Plantillas", "herramientas"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Inter",
        code: "JetBrains Mono",
      },
      // Colores parecidos a los temas por defecto de Obsidian
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#e0e0e0",
          gray: "#ababab",
          darkgray: "#4a4a4a",
          dark: "#222222",
          secondary: "#7a52e8",
          tertiary: "#9b7bf3",
          highlight: "rgba(138, 92, 245, 0.10)",
          textHighlight: "#ffe36688",
        },
        darkMode: {
          light: "#1e1e1e",
          lightgray: "#363636",
          gray: "#6b6b6b",
          darkgray: "#d6d6d6",
          dark: "#f0f0f0",
          secondary: "#a88bfa",
          tertiary: "#7f6df2",
          highlight: "rgba(168, 139, 250, 0.12)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: false,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
