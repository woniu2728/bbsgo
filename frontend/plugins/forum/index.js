import { renderForumHome } from "./pages/ForumHome.js";
import { renderPostDetail } from "./pages/PostDetail.js";

export const plugin = {
  name: "forum",
  routes: [
    { path: "/forum", render: renderForumHome },
    { path: "/forum/:id", render: renderPostDetail },
  ],
  menu: [{ id: "forum", label: "Forum", path: "/forum" }],
};
