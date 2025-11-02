import { useEffect, useMemo, useState, useCallback } from "react";
import { BookmarkContext } from "./BookmarkContext";
import axios from "../api/axios";
import { useAuth } from "../hooks/useAuth";

export function BookmarkProvider({ children }) {
  const { user, isLoading } = useAuth();
  const [bookmarks, setBookmarks] = useState([]);

  console.log("[BookmarkProvider] Rendering with received state:", { isLoading, user });

  // Sync bookmarks from user data on login, only when auth loading is complete
  useEffect(() => {
    console.log("[BookmarkProvider] useEffect running. isLoading:", isLoading);
    if (!isLoading) {
      if (user && user.bookmarks) {
        console.log("[BookmarkProvider] User data is available, syncing bookmarks.", user.bookmarks);
        const userBookmarks = user.bookmarks.map(b => ({ id: b.quote_id }));
        setBookmarks(userBookmarks);
      } else {
        console.log("[BookmarkProvider] No user or no bookmarks, clearing local bookmarks.");
        setBookmarks([]);
      }
    }
  }, [user, isLoading]);

  const toggleBookmark = useCallback(async (quote) => {
    if (!user) {
      alert("로그인이 필요한 기능입니다.");
      return null;
    }

    console.log(`[BookmarkProvider] Toggling bookmark for quote ID: ${quote.id}`);
    try {
      const response = await axios.post("/bookmark/toggle", {
        user_id: user.id,
        quote_id: quote.id,
      });
      console.log("[BookmarkProvider] Toggle API response:", response.data);

      // Update local state based on response
      if (response.data.bookmarked) {
        setBookmarks((prev) => [...prev, { id: quote.id }]);
      } else {
        setBookmarks((prev) => prev.filter((b) => b.id !== quote.id));
      }
      return response.data; // Return the new state
    } catch (error) {
      console.error("Failed to toggle bookmark:", error);
      alert("북마크 변경에 실패했습니다.");
      return null;
    }
  }, [user]);

  const isBookmarked = useCallback(
    (id) => bookmarks.some((q) => q.id === id),
    [bookmarks]
  );

  const value = useMemo(
    () => ({
      bookmarks,
      toggleBookmark,
      isBookmarked,
    }),
    [bookmarks, toggleBookmark, isBookmarked]
  );

  return (
    <BookmarkContext.Provider value={value}>
      {children}
    </BookmarkContext.Provider>
  );
}
