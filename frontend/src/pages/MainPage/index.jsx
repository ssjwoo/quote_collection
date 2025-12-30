import { useEffect, useState } from "react";
import { Search } from "../../components/Search";
import { Popular } from "./layout/Popular";
import { New } from "./layout/New";
import { Recommend } from "./layout/Recommend";
import { AIRecommend } from "./layout/AIRecommend";
import axios from "../../api/axios";

export const MainPage = ({ mode }) => {
  const [popularQuote, setPopularQuote] = useState({});
  const [newQuote, setNewQuote] = useState([]);
  const [recomQuote, setRecomQuote] = useState([]);

  /** mode에 맞게 데이터 불러오기 */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });

    const fetchQuotes = async () => {
      const promises = [
        axios.get(`/quote/popular/today/${mode}`),
        axios.get(`/quote/latest?source_type=${mode}`),
        axios.get(`/recommendations/?source_type=${mode}&limit=3`),
      ];

      const results = await Promise.allSettled(promises);

      if (results[0].status === "fulfilled") {
        setPopularQuote(results[0].value.data);
      }

      if (results[1].status === "fulfilled") {
        const sortedNew = results[1].value.data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );
        setNewQuote(sortedNew.slice(0, 3));
      }

      if (results[2] && results[2].status === "fulfilled") {
        setRecomQuote(results[2].value.data);
      }
    };

    fetchQuotes();
  }, [mode]);
  return (
    <>
      <div className="flex justify-center">
        <Search source_type={mode} />
      </div>
      <div className="mt-12">
        <Popular mode={mode} popularQuote={popularQuote} />
        <New mode={mode} newQuote={newQuote} />
        <Recommend mode={mode} recomQuote={recomQuote} />
        {/* AI Recommendation Section */}
        <AIRecommend />
      </div>
    </>
  );
};
