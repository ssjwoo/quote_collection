import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const RecommendDetail = ({mode}) => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);

   const onDetail=(id)=>{
        navigation('/quote/'+id, {
    state: {
      mode:mode
    }})
    }

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const token = localStorage.getItem("accesstoken");
        // TODO: /api/recommendations/user-based - need testing
        const response = await axios.get("/api/recommendations/user-based", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("/api/recommendations/user-based", response);
        setQuotes(response.data);
      } catch (error) {
        console.error("Failed to fetch recommendations:", error);
      }
    };

    fetchRecommendations();
  }, []);
  return (
    <>
      <div className="flex-col flex items-center mb-12">
        <div className="mt-16 mb-4 text-3xl">User Based Recommend</div>
        {quotes.map((quote) => (
          <div
            key={quote.id}
            className="mt-5 cursor-pointer w-11/12 border-2 border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg hover:bg-main-beige"
            onClick={() => onDetail(quote.id)}
          >
            <div>{quote.content}</div>
          </div>
        ))}
      </div>
    </>
  );
};
