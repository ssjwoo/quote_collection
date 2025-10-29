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
      try {
        const popularResponse = await axios.get(
          `/api/quote/popular/today/${mode}`
        );
        // console.log(`/api/quote/popular/today/${mode}`, popularResponse);
        // console.log("popularResposnse.data:", popularResponse.data);
        setPopularQuote(popularResponse.data); // Assuming it returns a single object

        // Fetch new quotes
        const newResponse = await axios.get(
          `/api/quote/latest?source_type=${mode}`
        );
        // console.log(`/api/quote/latest?source_type=${mode}`, newResponse);
        // console.log("newResponse.data:", newResponse.data);
        const sortedNew = newResponse.data.sort(
          (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
        );
        setNewQuote(sortedNew.slice(0, 3)); // Get top 3

        // Fetch recommended quotes
        const token = localStorage.getItem("token");
        if (token) {
          // TODO: /api/recommendations/user-based - need testing
          const recomResponse = await axios.get(
            "/api/recommendations/user-based",
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          console.log("/api/recommendations/user-based", recomResponse);
          setRecomQuote(recomResponse.data.slice(0, 3)); // Get top 3
        }
      } catch (error) {
        console.error("Failed to fetch quotes:", error);
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
        <Popular popularQuote={popularQuote} />
        <New newQuote={newQuote} />
        <Recommend recomQuote={recomQuote} />
      </div>
    </>
  );
};
