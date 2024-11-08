import { createContext, ReactNode, useState } from "react";

interface SidebarContextType {
  isOpen: boolean;
  toggleSidebar: (value?: boolean) => void;
}

export const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

export const SidebarProvider = ({ children }: { children: ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = (value?: boolean) => {
    if (typeof value === "boolean") {
      setIsOpen(value);
    } else {
      setIsOpen((prev) => !prev);
    }
  };

  return (
    <SidebarContext.Provider value={{ isOpen, toggleSidebar }}>
      {children}
    </SidebarContext.Provider>
  );
};