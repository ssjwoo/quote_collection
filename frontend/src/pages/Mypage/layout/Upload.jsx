import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const Upload = () => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(true);

  // 임시토큰 userId 1로 작동 테스트 // token방식 추가 필요
  useEffect(() => {
    const fetchUserAndQuotes = async () => {
      try {
        const userId = 1;
        const response = await axios.get(`/api/quote/user/${userId}`);
        console.log("MY Quote:", response.data);
        setQuotes(response.data);
      } finally {
        setLoading(false);
      }
    };

    fetchUserAndQuotes();
  }, []);

  const onDetail = (q) => {
    navigation(`/quote/${q.id}`, {
      state: {
        mode: q.source_type || "book",
      },
    });
  };

  return (
    <div className="flex flex-col items-center m-5">
      <h2 className="text-3xl font-semibold mb-6">My Quote</h2>

      {quotes.length === 0 ? (
        <div className="text-gray-500 mt-10">업로드 내용이 없습니다</div>
      ) : (
        <div className="grid grid-cols-1 gap-5 w-3/4">
          {quotes.map((q) => (
            <div
              key={q.id}
              className="cursor-pointer mt-3 border-2 border-main-green p-4 rounded-lg shadow-md hover:bg-main-beige transition-all"
              onClick={() => onDetail(q)}
            >
              <div className="text-lg font-medium mb-2">"{q.content}"</div>
              <div className="text-xs text-gray-500 text-end mt-2">
                등록일: {q.created_at ? q.created_at.slice(0, 10) : "N/A"}
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
};
