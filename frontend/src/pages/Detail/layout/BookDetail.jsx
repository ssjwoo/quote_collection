import { useNavigate } from 'react-router-dom';
import mark from '../../../assets/bookmark.png';
import marked from '../../../assets/bookmark_marked.png';
import { useEffect, useState } from 'react';
import { useBookmarks } from '../../../hooks/useBookmarks';

export const BookDetail = ({ quote }) => {
  const navigation = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [bookmark, setBookMarked] = useState(false);
  const [user, setUser] = useState({});
  const { isBookmarked, add, remove } = useBookmarks();

  useEffect(() => {
    const saved = localStorage.getItem('isLogin');
    if (saved != null) setIsLogin(saved === '1');
  }, []);

  useEffect(() => {
    if (quote?.id != null) {
      // dummy 사용자
      setUser({ id: 'user1', bookmark: { book: [1, 2, 3], funny: [1, 2] } });
      setBookMarked(isBookmarked(quote.id));
    }
  }, [quote?.id, isBookmarked]);

  const onIsLogin = () => {
    if (!isLogin) {
      const ok = confirm('로그인이 필요한 기능입니다. (임시) 로그인할까요?');
      if (!ok) return;
      setIsLogin(true);
      localStorage.setItem('isLogin', '1');
    }

    /** DB 사용자 북마크 데이터 업데이트는 나중 단계에서 */
    setBookMarked((prev) => {
      const next = !prev;
      if (quote?.id != null) {
        const mini = {
          id: quote.id,
          content: quote.content ?? '',
          sourceTitle: quote?.source?.title ?? '',
        };
        next ? add(mini) : remove(quote.id);
      }
      return next;
    });
  };


  const onSearchList = (input) => {
    navigation('/searchlist/' + input);
  };

  const onModify = () => {
    navigation('/detail/' + quote.id + '/modi');
  };

  const onDelete = () => {
    // TODO
  };

  return (
    <>
      <div className="flex flex-col mt-10">
        <div className="text-3xl mb-5">BOOK MOMENT</div>

        {user.id == quote.writer && (
          <div className="text-end">
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-2"
              onClick={onModify}
            >
              수정
            </button>
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs"
              onClick={onDelete}
            >
              삭제
            </button>
          </div>
        )}

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-sm text-end pb-3">책 제목 </label>
          <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
            <span className="cursor-pointer" onClick={() => onSearchList(quote.title)}>
              {quote.title}
            </span>
          </div>
        </div>

        <div className="flex justify-center mt-3">
          <div className="w-4/5 text-main-white pt-12 pb-12 bg-main-green rounded-lg p-2 pl-4 ml-3 shadow-lg shadow-gray-400">
            {quote.content}
          </div>
        </div>

        <div className="flex justify-end mt-3">
          <div className="flex border-2 border-sub-darkgreen rounded-lg p-3 mr-14">
            <img className="size-5 cursor-pointer" onClick={onIsLogin} src={(isLogin&&bookmark)?marked:mark}/>
          </div>
        </div>

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">저자 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span className="cursor-pointer" onClick={() => onSearchList(quote.creater)}>
              {quote.creater}
            </span>
          </div>
        </div>

        {quote.subData && (
          <>
            <div className="flex items-end mt-3">
              <label className="w-1/12 text-end pb-3 text-sm">출판사 </label>
              <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
                {quote.subData}
              </div>
            </div>
          </>
        )}

        {quote.tags && (
          <div className="flex items-end mt-3">
            <label className="w-1/12 text-end text-sm pb-3">TAGS </label>
            <div className="w-4/6 text-start rounded-lg p-2 pl-4 ">
              {quote.tags.map((t) => (
                <span
                  key={String(t?.id ?? t)}
                  onClick={() => onSearchList(t)}
                  className="cursor-pointer rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border"
                >
                  {String(t?.name ?? t)}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};
