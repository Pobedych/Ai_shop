import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Users,
  Package,
  ShoppingCart,
  TrendingUp,
} from "lucide-react";
import { prisma } from "@/lib/db";

export default async function DashboardPage() {
  // Получаем реальную статистику из базы данных
  const [totalUsers, activeItems, outOfStockItems] = await Promise.all([
    prisma.users.count(),
    prisma.items.count({ where: { count: { gt: 0 } } }),
    prisma.items.count({ where: { count: 0 } }),
  ]);

  const stats = [
    {
      title: "Всего пользователей",
      value: totalUsers.toString(),
      description: "Зарегистрировано в боте",
      icon: Users,
    },
    {
      title: "Товаров в наличии",
      value: activeItems.toString(),
      description: `Всего позиций: ${activeItems + outOfStockItems}`,
      icon: Package,
    },
    {
      title: "Заказы",
      value: "Скоро...",
      description: "Модель заказов пока не обнаружена",
      icon: ShoppingCart,
    },
    {
      title: "Выручка",
      value: "Скоро...",
      description: "Интеграция с платежами",
      icon: TrendingUp,
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Обзор</h2>
        <p className="text-muted-foreground">
          Добро пожаловать! Вот что сейчас происходит в твоем магазине.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Последние действия</CardTitle>
            <CardDescription>
              Последние регистрации и обновления товаров.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center border-2 border-dashed rounded-md">
              Здесь будет график активности
            </div>
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Топ товаров</CardTitle>
            <CardDescription>
              Позиции с самым большим остатком.
            </CardDescription>
          </CardHeader>
          <CardContent>
             <div className="space-y-4">
                {(await prisma.items.findMany({ take: 3, orderBy: { count: 'desc' } })).map((item, i) => (
                   <div key={item.id} className="flex items-center gap-4">
                      <div className="h-9 w-9 rounded bg-muted flex items-center justify-center font-bold">
                        {i + 1}
                      </div>
                      <div className="flex-1 space-y-1">
                        <p className="text-sm font-medium leading-none">{item.name}</p>
                        <p className="text-xs text-muted-foreground">{item.count} шт. в наличии</p>
                      </div>
                      <div className="font-medium">$ {item.price.toString()}</div>
                   </div>
                ))}
             </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
