import { useEffect, useState } from "react";
import { BookModi } from "./layout/BookModi";
import { DramaModi } from "./layout/DramaModi";
import { useParams } from "react-router-dom";
import { MovieModi } from "./layout/MovieModi";
import axios from "../../api/axios";

export const Modify = () => {
  const { id } = useParams();

  const [quote, setQuote] = useState(null);

  useEffect(() => {
    const fetchQuote = async () => {
      try {
        // TODO: /api/quote/${id}, no navigation
        const response = await axios.get(`/quote/${id}`);
        console.log(`/api/quote/${id}`, response);
        const data = response.data;
        let sourceType = "";
        if (data.source.book) {
          sourceType = "book";
        } else if (data.source.movie) {
          sourceType = "movie";
        } else if (data.source.drama) {
          sourceType = "drama";
        }
        setQuote({ ...data, sourceType });
      } catch (error) {
        console.error("Failed to fetch quote:", error);
      }
    };

    fetchQuote();
  }, [id]);

  return (
    <>
      {quote && (
        <>
          {quote.sourceType === "book" && <BookModi quote={quote} />}
          {quote.sourceType === "drama" && <DramaModi quote={quote} />}
          {quote.sourceType === "movie" && <MovieModi quote={quote} />}
        </>
      )}
    </>
  );
};
