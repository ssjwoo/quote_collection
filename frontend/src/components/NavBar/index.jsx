import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "book", color: "first", darkColor: "first" },
  { to: "/movie", label: "movie", color: "second", darkColor: "second" },
  { to: "/drama", label: "drama", color: "third", darkColor: "third" },
];

const colorVariants = {
  first: { bg: "bg-first-menu-dim", text: "text-gray-600" },
  activeFirst: { bg: "bg-first-menu-thick", text: "text-gray-800" },
  second: { bg: "bg-second-menu-dim", text: "text-gray-600" },
  activeSecond: { bg: "bg-second-menu-thick", text: "text-gray-800" },
  third: { bg: "bg-third-menu-dim", text: "text-gray-600" },
  activeThird: { bg: "bg-third-menu-thick", text: "text-gray-800" },
};

const NavBar = () => {
  return (
    <>
      <nav className="absolute -left-10 top-24">
        <ul className="space-y-4">
          {navItems.map((item, index) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                end
                style={{ transform: `translateX(${index * 4}px)` }}
                className={({ isActive }) => {
                  const variant = isActive
                    ? colorVariants[
                        `active${
                          item.darkColor.charAt(0).toUpperCase() +
                          item.darkColor.slice(1)
                        }`
                      ]
                    : colorVariants[item.color];
                  return (
                    `relative block w-12 h-26 py-3 px-2 text-center font-bold shadow-lg transition-transform duration-200 ease-in-out rounded-lg ` +
                    `[writing-mode:vertical-lr] text-sm ` +
                    `${variant.bg} ${variant.text} ` +
                    (isActive ? "z-20 scale-105" : "z-0")
                  );
                }}
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
};

export default NavBar;
