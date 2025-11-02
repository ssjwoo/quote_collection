import { NavLink, useNavigate } from "react-router-dom";

export const MyNavBar = ({ setIsOpen, isLogIn, setIsLogin }) => {
  const navigation = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    alert("로그아웃 되었습니다");
    setIsLogin(false);
    navigation("/");
    localStorage.setItem("accessToken", "");
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
      <nav className="float-right relative flex flex-row justify-items-end mr-1 mt-3 text-sm z-20">
        <div className="px-1 mr-1 cursor-pointer" onClick={onBookmark}>
          bookmark
        </div> |
        <div className="px-1 mr-1 cursor-pointer" onClick={onWrite}>
          write
        </div> |
        {isLogIn ? (
          <>
            <NavLink className="mr-1 px-1 cursor-pointer" to="/mypage/memberinfo">
              mypage
            </NavLink> 
            <span className="mr-2 ml-1.5 px-2 cursor-pointer border rounded-3xl" onClick={handleLogout}>
              logout
            </span>
          </>
        ) : (
          <>
            <span
              className="mr-1 px-1 cursor-pointer"
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
