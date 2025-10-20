import { useState } from "react";
import { addMark, newBookmark } from "../pages/Utils/newBookmark";

export function useBookmarkTree() {
  const [tree, setTree] = useState({ id: "root", name: "Bookmark", children: [] });
  const [addAtId, setAddAtId] = useState("root");

  const createFolderAt = (targetId, name) => {
    const trimmed = name.trim();
    if (!trimmed) return;
    const node = newBookmark(trimmed);
    setTree((prev) => addMark(prev, targetId, node));
    setAddAtId(node.id); // 생성 포인터를 방금 만든 폴더로 이동
  };

  return { tree, addAtId, setAddAtId, createFolderAt };
}
