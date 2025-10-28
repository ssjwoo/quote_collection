import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBookmarkTree } from "../../../hooks/useBookmarkTree";
import NameModal from "../../../components/Modal/NameModal/index.jsx";

export function BookMark() {
  const { tree, createFolderAt } = useBookmarkTree();
  const [modalOpen, setModalOpen] = useState(false);
  const [targetId, setTargetId] = useState(null);
  const navigate = useNavigate();

  const openModalAt = (id) => {
    setTargetId(id);
    setModalOpen(true);
  };
  const confirmCreate = (name) => {
    if (targetId != null) createFolderAt(targetId, name);
    setModalOpen(false);
    setTargetId(null);
  };

  const [q, setQ] = useState("");
  const [sort, setSort] = useState("recent");

  const rootId = tree?.id ?? tree?.key ?? null;
  const topGroups = useMemo(() => {
    const children = Array.isArray(tree?.children) ? tree.children : [];
    return children
      .map((c) => ({
        id: c.id ?? c.key,
        name: c.name ?? c.title ?? "(이름없음)",
      }))
      .filter((g) => g.id != null);
  }, [tree]);

  return (
    <div className="p-6 mt-4 mx-auto max-w-6xl">
      <h1 className="text-3xl font-medium mb-6 text-center">Bookmark</h1>

      <div className="mb-8 flex flex-col items-end gap-3">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="내용/출처 검색"
          className="text-sm border rounded px-2 py-2 w-full sm:w-64"
        />
        <div className="flex items-center gap-2">
          <label className="text-sm">정렬</label>
          <select
            className="text-sm border rounded px-2 py-2"
            value={sort}
            onChange={(e) => setSort(e.target.value)}
          >
            <option value="recent">최신순</option>
            <option value="alpha">가나다</option>
          </select>
        </div>
      </div>

      <div className="mx-auto sm:mx-0 max-w-sm sm:max-w-none">
        <div className="grid grid-cols-2 gap-4">
          {topGroups.map((g) => (
            <button
              key={g.id}
              type="button"
              title={`${g.name} 열기`}
              onClick={() => navigate(`/mypage/bookmark/group/${g.id}`)}
              className="w-full h-14 rounded-lg border border-main-green bg-custom-pink hover:bg-main-beige text-sm flex items-center justify-center px-3 whitespace-nowrap overflow-hidden text-ellipsis truncate"
            >
              {g.name}
            </button>
          ))}

          <button
            type="button"
            title="새 폴더 만들기"
            onClick={() => openModalAt(rootId)}
            className="w-full h-14 rounded-lg border border-dashed hover:bg-gray-50 text-sm flex items-center justify-center"
            aria-label="새 폴더"
          >
            +
          </button>
        </div>
      </div>

      <NameModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onConfirm={confirmCreate}
      />

      <p className="mt-10 text-sm text-gray-600 text-center">
        폴더를 클릭하면 해당 폴더에 담긴 북마크를 볼 수 있어요.
      </p>
    </div>
  );
}
