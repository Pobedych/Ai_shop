"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Users,
  Package,
  ShoppingCart,
  Settings,
  LogOut,
} from "lucide-react";
import { buttonVariants } from "@/components/ui/button";

const navItems = [
  {
    label: "Overview",
    icon: LayoutDashboard,
    href: "/",
  },
  {
    label: "Users",
    icon: Users,
    href: "/users",
  },
  {
    label: "Products",
    icon: Package,
    href: "/products",
  },
  {
    label: "Orders",
    icon: ShoppingCart,
    href: "/orders",
  },
  {
    label: "Settings",
    icon: Settings,
    href: "/settings",
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-card h-screen sticky top-0 overflow-y-auto flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold tracking-tight">Ai-shop Admin</h1>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              buttonVariants({ variant: "ghost" }),
              "w-full justify-start gap-3",
              pathname === item.href
                ? "bg-accent text-accent-foreground font-medium"
                : "text-muted-foreground hover:text-foreground"
            )}
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t">
        <button
          className={cn(
            buttonVariants({ variant: "ghost" }),
            "w-full justify-start gap-3 text-destructive hover:text-destructive hover:bg-destructive/10"
          )}
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </aside>
  );
}
