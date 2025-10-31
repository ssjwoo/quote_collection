import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { BookDetail } from "./layout/BookDetail";
import { MovieDetail } from "./layout/MovieDetail";
import { DramaDetail } from "./layout/DramaDetail";
import { RecommendDetail } from "./layout/RecommendDetail";
import axios from "../../api/axios";

export const Detail = () => {
  /** id로 해당 data 불러오기  */
  const { id } = useParams();
  const location = useLocation();
  const mode = location.state?.mode;
  console.log(mode);

  const [quote, setQuote] = useState(null);

  useEffect(() => {
    const fetchQuote = async () => {
      try {
        // TODO: /api/quote/${id} - need testing
        const response = await axios.get(`/quote/${id}`);
        console.log(`/api/quote/${id}`, response);
        const data = response.data;
        setQuote(data);
      } catch (error) {
        console.error("Failed to fetch quote:", error);
      }
    };

    fetchQuote();
  }, [id]);

  if (!quote) {
    return <div>Loading...</div>; // Or a more sophisticated loading indicator
  }

  return (
    <>
      {mode == "book" && <BookDetail quote={quote} />}
      {mode == "movie" && <MovieDetail quote={quote} />}
      {mode == "drama" && <DramaDetail quote={quote} />}
      <RecommendDetail mode={mode} quote={quote} />
    </>
  );
};
