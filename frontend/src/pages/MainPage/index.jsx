import { useEffect, useState } from "react";
import { Search } from "../../components/Search";
import { Popular } from "./layout/Popular";
import { New } from "./layout/New";
import { Recommend } from "./layout/Recommend";
import axios from "../../api/axios";

export const MainPage = ({ mode }) => {
  const [popularQuote, setPopularQuote] = useState({});
  const [newQuote, setNewQuote] = useState([]);
  const [recomQuote, setRecomQuote] = useState([]);

  /** mode에 맞게 데이터 불러오기 */
  useEffect(() => {
    const fetchQuotes = async () => {
      const token = localStorage.getItem("accessToken");

      const promises = [
        axios.get(`/api/quote/popular/today/${mode}`),
        axios.get(`/api/quote/latest?source_type=${mode}`),
      ];

      if (token) {
        promises.push(
          axios.get("/api/recommendations/user-based", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
        );
      }

      const results = await Promise.allSettled(promises);

      if (results[0].status === "fulfilled") {
        setPopularQuote(results[0].value.data);
      } else {
        console.error("Failed to fetch popular quotes:", results[0].reason);
      }

      if (results[1].status === "fulfilled") {
        const sortedNew = results[1].value.data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );
        setNewQuote(sortedNew.slice(0, 3));
      } else {
        console.error("Failed to fetch new quotes:", results[1].reason);
      }

      if (token && results[2] && results[2].status === "fulfilled") {
        setRecomQuote(results[2].value.data.slice(0, 3));
      } else if (token && results[2]) {
        console.error("Failed to fetch recommended quotes:", results[2].reason);
      }
    };

    fetchQuotes();
  }, [mode]);
  return (
    <>
      <div className="flex justify-center">
        <Search />
      </div>
      <div className="mt-12">
        <Popular mode={mode} popularQuote={popularQuote} />
        <New mode={mode} newQuote={newQuote} />
        <Recommend mode={mode} recomQuote={recomQuote} />
      </div>
    </>
  );
};
