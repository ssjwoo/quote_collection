import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../../../api/axios";
import { Pagination } from "../../../components/Pagination";

export const Upload = ({ userId }) => {
  const navigation = useNavigate();
  const [quotes, setQuotes] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!userId) return;

    const fetchQuotes = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`/quote/user/${userId}?page=${currentPage}&size=10`);
        setQuotes(response.data.items);
        setTotal(response.data.total);
        setTotalPages(response.data.total_pages);
      } catch (error) {
        console.error("Failed to fetch uploaded quotes:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuotes();
  }, [userId, currentPage]);

  const onDetail = (id) => {
    navigation("/quote/" + id);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  return (
    <div className="p-2 md:p-6">
      <div className="mb-4 text-right text-sm text-gray-500">
        전체 {total}개
      </div>

      <div className="flex flex-col justify-items-center m-1 md:m-3 min-h-[400px]">
        {isLoading ? (
          <div className="flex justify-center items-center h-40 font-medium text-main-green">Loading...</div>
        ) : quotes.length > 0 ? (
          <>
            {quotes.map((q) => (
              <div
                key={q.id}
                className="cursor-pointer mt-5 border-2 hover:bg-mypage-menu/50 border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg active:scale-[0.98] transition-all"
                onClick={() => onDetail(q.id)}
              >
                <div className="text-lg px-4 font-medium">{q.content}</div>
                {q.source && (
                  <div className="text-sm text-gray-500 mt-2 italic">
                    - {q.source.title} ({q.source.creator})
                  </div>
                )}
              </div>
            ))}

            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          </>
        ) : (
          <p className="text-center py-20 text-gray-400">업로드한 인용문이 없습니다.</p>
        )}
      </div>
    </div>
  );
};
