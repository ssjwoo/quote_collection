import { useEffect, useMemo, useState, useCallback } from "react";
import { BookmarkContext } from "./BookmarkContext";

export function BookmarkProvider({ children }) {
  const [bookmarks, setBookmarks] = useState(() => {
    if (typeof window === "undefined") return [];
    try {
      const raw = window.localStorage.getItem("bookmarks");
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      console.warn("Failed to parse bookmarks from storage:", e);
      return [];
    }
  });

  const [bookmarkFolders, setBookmarkFolders] = useState(() => {
    if (typeof window === "undefined") return {};
    try {
      const raw = window.localStorage.getItem("bookmarkFolders");
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  });   
  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem(
        "bookmarkFolders",
        JSON.stringify(bookmarkFolders)
      );
    } catch (e) {e}
  }, [bookmarkFolders]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem("bookmarks", JSON.stringify(bookmarks));
    } catch (e) {
      console.warn("Failed to persist bookmarks:", e);
    }
  }, [bookmarks]);

  const add = useCallback((quote) => {
    setBookmarks((prev) => {
      if (prev.some((q) => q.id === quote.id)) return prev;
      const tags = Array.isArray(quote?.tags)
        ? quote.tags.map((t) =>
            typeof t === "string" ? t : t?.name ?? String(t)
          )
        : [];
      const mini = {
        id: quote.id,
        content: quote.content ?? "",
        sourceTitle: quote.sourceTitle ?? quote?.source?.title ?? "",
        createdAt: quote.createdAt ?? Date.now(),
        tags,
      };
      return [...prev, mini];
    });
  }, []);

  const remove = useCallback((id) => {
    setBookmarks((prev) => prev.filter((q) => q.id !== id));
    setBookmarkFolders((prev) => {
      if (!(id in prev)) return prev;
      const next = { ...prev };
      delete next[id];
      return next;
    });
  }, []);

  const toggle = useCallback((quote) => {
    setBookmarks((prev) => {
      const exists = prev.some((q) => q.id === quote.id);
      if (exists) return prev.filter((q) => q.id !== quote.id);
      const tags = Array.isArray(quote?.tags)
        ? quote.tags.map((t) =>
            typeof t === "string" ? t : t?.name ?? String(t)
          )
        : [];
      const mini = {
        id: quote.id,
        content: quote.content ?? "",
        sourceTitle: quote.sourceTitle ?? quote?.source?.title ?? "",
        createdAt: quote.createdAt ?? Date.now(),
        tags,
      };
      return [...prev, mini];
    });
  }, []);

  const assignFolder = useCallback((bookmarkId, folderId) => {
    setBookmarkFolders((prev) => ({ ...prev, [bookmarkId]: folderId ?? null }));
  }, []);
  const getFolder = useCallback(
    (bookmarkId) => bookmarkFolders?.[bookmarkId] ?? null,
    [bookmarkFolders]
  );

  const isBookmarked = useCallback(
    (id) => bookmarks.some((q) => q.id === id),
    [bookmarks]
  );

  const value = useMemo(
    () => ({
      bookmarks,
      add,
      remove,
      toggle,
      isBookmarked,
      assignFolder,
      getFolder,
      bookmarkFolders,
    }),
    [
      bookmarks,
      add,
      remove,
      toggle,
      isBookmarked,
      assignFolder,
      getFolder,
      bookmarkFolders,
    ]
  );

  return (
    <BookmarkContext.Provider value={value}>
      {children}
    </BookmarkContext.Provider>
  );
}
