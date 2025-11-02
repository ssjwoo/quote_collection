import { Link} from "react-router-dom";
import { LoginInput } from "../../LoginInput";
import axios from "../../../api/axios";

const LoginModal = ({ setIsLogin, setIsOpen }) => {

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const email = form.email.value;
    const password = form.password.value;

    try {
      const response = await axios.post(
        "/auth/login",
        new URLSearchParams({
          username: email,
          password: password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      console.log("/api/auth/login", response);
      localStorage.setItem("accessToken", response.data.access_token);
      setIsLogin(true);
      setIsOpen(false);
    } catch  {
      alert("로그인 정보가 없습니다.");
    }
  };

  return (
    <>
      <div
        className="fixed inset-0 z-[9999] flex justify-center items-center bg-black/50"
        onClick={() => setIsOpen(false)}
      >
        <div onClick={(e) => e.stopPropagation()}>
          <div className="mb-6 bg-main-green/80 h-[330px] w-[350px] rounded-sm flex-col flex items-start md:items-center justify-between md:justify-center">
            <div className="text-custom-div text-3xl mb-5 cursor-pointer">
              LOGIN
            </div>

            <form className="space-y-4 " onSubmit={handleSubmit}>
              <LoginInput title="email" type="email" name="email" />
              <div className="flex items-center mb-5">
                <LoginInput title="password" type="password" name="password" />
                <button className="border ml-3 mt-5 border-custom-div text-custom-div w-[70px] h-[30px] rounded-sm flex justify-center items-center hover:bg-custom-div hover:text-main-green transition">
                  login
                </button>
                <div></div>
              </div>
            </form>

            <div className="flex mb-5">
              <div className="mr-3 text-white text-sm">
                아직 회원이 아니시라면?
              </div>
              <div className="text-custom-bold-font underline text-sm">
                <Link to="/signup">join us</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginModal;
