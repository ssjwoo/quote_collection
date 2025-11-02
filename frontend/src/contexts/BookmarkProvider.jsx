import { useEffect, useMemo, useState, useCallback } from "react";
import { BookmarkContext } from "./BookmarkContext";
import axios from "../api/axios";
import { useAuth } from "../hooks/useAuth";

export function BookmarkProvider({ children }) {
  const { user } = useAuth();
  const [bookmarks, setBookmarks] = useState([]);

  // Sync bookmarks from user data on login
  useEffect(() => {
    if (user && user.bookmarks) {
      const userBookmarks = user.bookmarks.map(b => ({ id: b.quote_id }));
      setBookmarks(userBookmarks);
    } else {
      setBookmarks([]);
    }
  }, [user]);

  const toggleBookmark = useCallback(async (quote) => {
    if (!user) {
      alert("로그인이 필요한 기능입니다.");
      return;
    }

    try {
      const response = await axios.post("/bookmark/toggle", {
        user_id: user.id,
        quote_id: quote.id,
      });

      // Update local state based on response
      if (response.data.bookmarked) {
        setBookmarks((prev) => [...prev, { id: quote.id }]);
      } else {
        setBookmarks((prev) => prev.filter((b) => b.id !== quote.id));
      }
    } catch (error) {
      console.error("Failed to toggle bookmark:", error);
      alert("북마크 변경에 실패했습니다.");
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
