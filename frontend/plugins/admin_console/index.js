import { renderAdminHome } from "./pages/Home.js";
import { renderPlugins } from "./pages/Plugins.js";
import { renderBoards } from "./pages/Boards.js";
import { renderThemes } from "./pages/Themes.js";
import { renderSeo } from "./pages/Seo.js";

export const plugin = {
  name: "admin-console",
  routes: [
    { path: "/admin", render: renderAdminHome },
    { path: "/admin/plugins", render: renderPlugins },
    { path: "/admin/forums", render: renderBoards },
    { path: "/admin/themes", render: renderThemes },
    { path: "/admin/seo", render: renderSeo },
  ],
  menu: [{ id: "admin", label: "Admin", path: "/admin" }],
};
