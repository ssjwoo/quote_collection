import { useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useBookmarks } from "../../../hooks/useBookmarks.js";
import { useBookmarkTree } from "../../../hooks/useBookmarkTree";

export default function BookmarkGroup() {
  const { folderId } = useParams();
  const navigate = useNavigate();
  const { bookmarks, remove, assignFolder, getFolder } = useBookmarks();
  const { tree } = useBookmarkTree();

  const findById = (node, id) => {
    if (!node) return null;
    const nid = String(node.id ?? node.key ?? "");
    if (nid === String(id)) return node;
    for (const c of node.children ?? []) {
      const f = findById(c, id);
      if (f) return f;
    }
    return null;
  };
  const folder = useMemo(() => findById(tree, folderId), [tree, folderId]);
  const folderName = folder?.name ?? folder?.title ?? "(알 수 없는 그룹)";

  const [q, setQ] = useState("");
  const [sort, setSort] = useState("recent");
  const [activeTag, setActiveTag] = useState(null);

  const allTags = useMemo(() => {
    const s = new Set();
    bookmarks.forEach((b) => (b.tags ?? []).forEach((t) => s.add(String(t))));
    return Array.from(s).sort((a, b) => a.localeCompare(b));
  }, [bookmarks]);

  const inThisFolder = useMemo(
    () => bookmarks.filter((b) => String(getFolder(b.id)) === String(folderId)),
    [bookmarks, folderId, getFolder]
  );

  const filtered = useMemo(() => {
    let base = inThisFolder.slice();
    if (activeTag) {
      base = base.filter((b) => (b.tags ?? []).map(String).includes(activeTag));
    }
    const needle = q.trim().toLowerCase();
    if (!needle) return base;
    return base.filter((b) =>
      `${b.content ?? ""} ${b.sourceTitle ?? ""}`.toLowerCase().includes(needle)
    );
  }, [inThisFolder, q, activeTag]);

  const sorted = useMemo(() => {
    const arr = filtered.slice();
    if (sort === "recent") arr.sort((a, b) => (b.createdAt ?? 0) - (a.createdAt ?? 0));
    else if (sort === "alpha") arr.sort((a, b) => (a.content ?? "").localeCompare(b.content ?? ""));
    return arr;
  }, [filtered, sort]);

  const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const highlight = (text, needle) => {
    const t = String(text ?? "");
    const n = needle.trim();
    if (!n) return t;
    const re = new RegExp(`(${escapeRegExp(n)})`, "ig");
    return t.split(re).map((part, i) =>
      i % 2 === 1 ? <mark key={i} className="bg-yellow-200">{part}</mark> : <span key={i}>{part}</span>
    );
  };

  const options = [
    { id: folderId, label: folderName },
    { id: "", label: "미지정" },
  ];

  return (
    <div className="p-6 mt-4 mx-auto max-w-6xl">
      <div className="mb-4 flex items-center gap-2">
        <button
          className="text-xs border px-2 py-1 rounded hover:bg-gray-50"
          onClick={() => navigate("/mypage/bookmark")}
          type="button"
        >
          ← back
        </button>
        <h1 className="text-2xl font-semibold">{folderName}</h1>
        <span className="text-sm opacity-70">({inThisFolder.length})</span>
      </div>


      <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="내용/출처 검색"
            className="text-sm border rounded px-2 py-1 w-44"
          />
          <label className="text-sm">정렬</label>
          <select
            className="text-sm border rounded px-2 py-1"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="recent">최신순</option>
            <option value="alpha">가나다</option>
          </select>
        </div>
        {allTags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setActiveTag(null)}
              className={`text-xs border px-2 py-1 rounded ${activeTag ? "opacity-70" : "bg-gray-100"}`}
            >
              모든 태그
            </button>
            {allTags.map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => setActiveTag((t) => (t === tag ? null : tag))}
                className={`text-xs border px-2 py-1 rounded ${
                  activeTag === tag ? "bg-main-beige" : "hover:bg-gray-50"
                }`}
              >
                #{tag}
              </button>
            ))}
          </div>
        )}
      </div>

      {sorted.length === 0 ? (
        <div className="text-sm text-gray-600">북마크가 존재하지 않습니다.</div>
      ) : (
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {sorted.map((item) => (
            <div key={item.id} className="rounded-2xl border bg-white/70 p-4 shadow-sm">
              <div className="text-xs opacity-60 mb-1 flex items-center justify-between">
                <span>
                  # {item.id}
                  {item.createdAt ? (
                    <span className="ml-2">{new Date(item.createdAt).toLocaleString()}</span>
                  ) : null}
                </span>
                <select
                  className="text-[11px] border rounded px-1 py-0.5"
                  value={String(getFolder(item.id) ?? "")}
                  onChange={(e) => assignFolder(item.id, e.target.value || null)}
                  title="그룹 지정"
                >
                  {options.map((opt) => (
                    <option key={String(opt.id)} value={opt.id}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="font-medium mb-2 break-words">
                {highlight(item.content || "(내용 없음)", q)}
              </div>
              {item.sourceTitle ? (
                <div className="text-xs opacity-80 mb-3">— {highlight(item.sourceTitle, q)}</div>
              ) : null}

              <div className="mt-2 flex gap-2">
                <button
                  type="button"
                  className="text-xs border px-2 py-1 rounded hover:bg-gray-50"
                  onClick={() => remove(item.id)}
                >
                  북마크 해제
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
