import { useEffect, useMemo, useState, useCallback } from "react";
import { BookmarkContext } from "./BookmarkContext";
import axios from "../api/axios";
import { useAuth } from "../hooks/useAuth";

export function BookmarkProvider({ children }) {
  const { user, isLoading, showAlert } = useAuth();
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
      // alert("로그인이 필요한 기능입니다.");
      showAlert("로그인이 필요한 기능입니다.");
      return null;
    }

    console.log(`[BookmarkProvider] Toggling bookmark for quote ID: ${quote.id}`);
    try {
      const payload = {
        user_id: user.id,
        quote_id: quote.id,
      };

      // If it's an AI Quote (negative ID), send quote data for creation
      if (quote.id <= 0) {
        console.log("[BookmarkProvider] Detected AI Quote, attaching data for creation.");
        payload.quote_data = {
          content: quote.content,
          // Handle source structure safely
          source_title: quote.source ? quote.source.title : "Unknown Source",
          author: quote.source ? quote.source.creator : "Unknown Author",
          source_type: quote.source ? quote.source.source_type : "book",
          // Handle tags safely
          tags: quote.tags ? quote.tags.map(t => t.name) : []
        };
      }

      const response = await axios.post("/bookmark/toggle", payload);
      console.log("[BookmarkProvider] Toggle API response:", response.data);

      // Update local state based on response
      if (response.data.bookmarked) {
        // If it was an AI quote, the ID might have changed (or we just bookmarked the real one)
        // But for local check, we might still have the negative ID in the list if we don't refresh.
        // Ideally, we should update with the real ID returned by backend if possible.
        // But for now, let's trust the toggle logic.
        // Wait, if backend created a new quote, response.data returns the bookmark object which has quote_id.
        // But the quote in frontend still has current ID.
        // If we bookmark -1, backend makes it 123. Bookmark is (user, 123).
        // Frontend list needs 123 to show it as bookmarked? 
        // No, frontend checks `isBookmarked(quote.id)`. If quote.id is still -1, and list has 123, it returns false.
        // So we might need to update the quote object's ID in the memory or add -1 to bookmarks list temporarily?
        // Or better, just rely on the fact that if we successfully bookmarked, we add the *original* ID to local state for instant feedback?
        // But if user refreshes, they get the new ID.
        // Let's stick to adding the *original* ID to local state for UI consistency until refresh.
        setBookmarks((prev) => [...prev, { id: quote.id }]);
      } else {
        setBookmarks((prev) => prev.filter((b) => b.id !== quote.id));
      }
      return response.data; // Return the new state
    } catch (error) {
      console.error("Failed to toggle bookmark:", error);
      // alert("북마크 변경에 실패했습니다.");
      showAlert("북마크 변경에 실패했습니다.");
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
