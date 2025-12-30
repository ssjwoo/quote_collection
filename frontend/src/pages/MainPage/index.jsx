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
        const res = await axios.get(`/quote/latest?source_type=${mode}`, { timeout: 60000 });
        const sortedNew = res.data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );
        setNewQuote(sortedNew.slice(0, 3));
      } catch (e) {
        console.error("Failed to fetch latest quotes", e);
      }
    };

    const fetchRecom = async () => {
      try {
        const res = await axios.get(`/recommendations/?source_type=${mode}&limit=6`, { timeout: 60000 });
        setRecomQuote(res.data);
      } catch (e) {
        console.error("Failed to fetch recommendations", e);
      }
    };


    setNewQuote([]);
    setRecomQuote([]);


    fetchLatest();
    fetchRecom();
  }, [mode]);
  return (
    <>
      <div className="flex justify-center">
        <Search source_type={mode} />
      </div>
      <div className="mt-12">

        <New mode={mode} newQuote={newQuote} />
        <Recommend mode={mode} recomQuote={recomQuote} />
        {/* AI Recommendation Section */}
        <AIRecommend />
      </div>
    </>
  );
};
