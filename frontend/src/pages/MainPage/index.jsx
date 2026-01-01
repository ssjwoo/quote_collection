import { useEffect, useState } from "react";
import { Search } from "../../components/Search";

import { New } from "./layout/New";
import { Recommend } from "./layout/Recommend";
import { AIRecommend } from "./layout/AIRecommend";
import axios from "../../api/axios";

export const MainPage = ({ mode }) => {

  const [newQuote, setNewQuote] = useState([]);
  const [recomQuote, setRecomQuote] = useState([]);

  /** mode에 맞게 데이터 불러오기 */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });

    const fetchLatest = async () => {
      try {
        // If mode is trends, we might want to fetch popular quotes instead
        const endpoint = mode === "trends" ? "/quote/popular/today/book" : `/quote/latest?source_type=book`;
        const res = await axios.get(endpoint, { timeout: 60000 });

        let data = res.data;
        // Adjust for PopularQuoteResponse structure if needed (it's a single object, but let's wrap in array for New component)
        if (mode === "trends") {
          data = data ? [data] : [];
        }

        const sortedNew = Array.isArray(data) ? data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        ) : [];
        setNewQuote(sortedNew.slice(0, 3));
      } catch (e) {
        console.error("Failed to fetch latest/popular quotes", e);
      }
    };

    const fetchRecom = async () => {
      try {
        // Always use 'book' for recommendations now
        const res = await axios.get(`/recommendations/?source_type=book&limit=6`, { timeout: 60000 });
        setRecomQuote(res.data);
      } catch (e) {
        console.error("Failed to fetch recommendations", e);
      }
    };

    setNewQuote([]);
    setRecomQuote([]);

    if (mode !== "ai-pick") {
      fetchLatest();
      fetchRecom();
    }
  }, [mode]);
  return (
    <>
      {mode !== "ai-pick" && (
        <div className="flex justify-center">
          <Search source_type={mode} />
        </div>
      )}
      <div className="mt-12">
        {mode === "ai-pick" ? (
          <AIRecommend />
        ) : (
          <>
            <New mode={mode} newQuote={newQuote} />
            <Recommend mode={mode} recomQuote={recomQuote} />
          </>
        )}
      </div>
    </>
  );
};
