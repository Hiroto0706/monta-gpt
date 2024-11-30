import Image from "next/image";

export enum IconMode {
  Open = "open",
  Close = "close",
}

interface Props {
  mode: IconMode;
  isOpen: boolean;
  toggleSidebar: (value?: boolean) => void;
}

const SidebarIcon: React.FC<Props> = ({ mode, isOpen, toggleSidebar }) => {
  const iconClass =
    mode === IconMode.Open ? `fixed ${isOpen ? "hidden" : ""}` : "absolute";
  return (
    <>
      <div
        className={`top-1 left-1 p-1 hover:bg-g ray-300 duration-300 rounded-lg cursor-pointer ${iconClass}`}
        onClick={() => toggleSidebar()}
      >
        <Image
          src={`/icons/sidebar-${mode}.png`}
          width={20}
          height={20}
          alt={`sidebar ${mode} button`}
        />
      </div>
    </>
  );
};

export default SidebarIcon;
