import { useNavigate } from "react-router-dom";
import SigninInput from "../SigninInput";
import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import axios from "../../api/axios";

export const Signup = () => {
  const navigation = useNavigate();
  const { signup, sevError } = useAuth();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
  });

  const [error, setError] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const validate = async () => {
    const newErrors = {};
    if(!form.username){
      newErrors.name = "이름을 입력해주세요.";
    }else{
    // name check api
    try {
      const response = await axios.post("/users/check-name", {
        username: form.username,
      });
      if (!response.data.is_available) {
        newErrors.name = "이미 사용중인 이름입니다.";
      }
    } catch (error) {
      console.error("name check error", error);
    }
    }
    

    if (
      !/^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i.test(
        form.email
      )
    ) {
      newErrors.email = "올바른 이메일 형식이 아닙니다.";
    }

    if (!/^(?=.*[a-zA-Z])(?=.*[0-9]).{8,}$/.test(form.password)) {
      newErrors.password = "영문자와 숫자를 포함해 8자 이상이어야 합니다.";
    }

    if (form.password !== form.passwordConfirm) {
      newErrors.passwordConfirm = "비밀번호가 일치하지 않습니다";
    }

    setError(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handlesubmit = async (e) => {
    e.preventDefault();

    if (!(await validate())) return;

    const { email, username, password } = form;
    const success = await signup({ email, username, password });

    if (success) {
      alert("회원가입이 완료되었습니다");
      navigation("/");
    } else {
      alert(sevError);
    }
  };

  return (
    <>
      <div className="min-h-screen flex justify-center items-start pt-12">
        <div className="w-full max-w-md rounded-xl p-8">
          <div className="mb-10 text-custom-basic-font text-3xl">Signup</div>

          <form
            className="flex-col items-center justify-center text-start ml-24"
            onSubmit={handlesubmit}
          >
            <SigninInput
              title="name"
              type="text"
              name="username"
              placeholder="이름을 입력해주세요"
              value={form.username}
              onChange={handleChange}
            />
            {error.name && (
              <p className="text-red-500 text-sm mt-1">{error.name}</p>
            )}
            <div className="">
              <SigninInput
                title="email"
                type="email"
                name="email"
                placeholder="이메일을 입력해주세요"
                value={form.email}
                onChange={handleChange}
              />
              {error.email && (
                <p className="text-red-500 text-sm mt-1">{error.email}</p>
              )}
              <SigninInput
                title="pw"
                type="password"
                name="password"
                placeholder="비밀번호를 입력해주세요"
                value={form.password}
                onChange={handleChange}
              />
              {error.password && (
                <p className="text-red-500 text-sm mt-1">{error.password}</p>
              )}
              <SigninInput
                title="pw confirm"
                type="password"
                name="passwordConfirm"
                placeholder="비밀번호를 다시 입력해주세요"
                value={form.passwordConfirm}
                onChange={handleChange}
              />
              {error.passwordConfirm && (
                <p className="text-red-500 text-sm mt-1">
                  {error.passwordConfirm}
                </p>
              )}
              <div className="mt-5">
                <button
                  onClick={() => navigation("/")}
                  type="button"
                  className="bg-custom-search mr-3 w-[80px] h-[30px]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-mypage-menu w-[80px] h-[30px] mt-5"
                >
                  Confirm
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};
