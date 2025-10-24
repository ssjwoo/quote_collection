import { NavLink, useNavigate } from "react-router-dom";
export const MyNavBar = ({ setIsOpen, isLogIn, setIsLogin }) => {
  const navigation = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    alert("로그아웃 되었습니다");
    setIsLogin(false);
  };

  const onBookmark = () => {
    if (!isLogIn) {
      alert("로그인이 필요한 기능입니다.");
    } else {
      navigation("/mypage/bookmark");
    }
  };

  const onWrite = () => {
    if (!isLogIn) {
      alert("로그인이 필요한 기능입니다.");
    } else {
      navigation("/write");
    }
  };

  return (
    <>
      <nav className="float-right relative flex flex-row justify-items-end mr-3 mt-3 text-sm z-20">
        <div className="mr-3 pr-2 pl-2 cursor-pointer" onClick={onBookmark}>
          bookmark
        </div>
        <div className="mr-3 pr-2 pl-2 cursor-pointer" onClick={onWrite}>
          write
        </div>
        {isLogIn ? (
          <>
            <NavLink className="mr-3 pr-2 pl-2 cursor-pointer" to="/mypage/memberinfo">
              mypage
            </NavLink>
            <span className="mr-3 pr-2 pl-2 cursor-pointer" onClick={handleLogout}>
              logout
            </span>
          </>
        ) : (
          <>
            <span
              className="mr-3 pr-2 pl-2 cursor-pointer"
              onClick={() => setIsOpen(true)}
            >
              login
            </span>
          </>
        )}
      </nav>
    </>
  );
};
