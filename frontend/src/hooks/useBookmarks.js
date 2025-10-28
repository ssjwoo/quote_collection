import { useContext } from "react";
import { BookmarkContext } from "../contexts/BookmarkContext";

export function useBookmarks() {
  const ctx = useContext(BookmarkContext);
  if (!ctx)
    throw new Error("useBookmarks must be used within BookmarkProvider");
  return ctx;
}