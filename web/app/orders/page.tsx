import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";

const orders = [
  {
    id: "ORD-001",
    customer: "John Doe",
    date: "2024-03-22 14:30",
    total: 119.98,
    status: "delivered",
    payment: "paid",
  },
  {
    id: "ORD-002",
    customer: "Jane Smith",
    date: "2024-03-22 15:45",
    total: 19.99,
    status: "processing",
    payment: "paid",
  },
  {
    id: "ORD-003",
    customer: "Alex Johnson",
    date: "2024-03-23 09:15",
    total: 149.99,
    status: "pending",
    payment: "pending",
  },
];

export default function OrdersPage() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "delivered": return "bg-green-500/10 text-green-500 border-green-500/20";
      case "processing": return "bg-blue-500/10 text-blue-500 border-blue-500/20";
      case "pending": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20";
      case "cancelled": return "bg-red-500/10 text-red-500 border-red-500/20";
      default: return "";
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Orders</h2>
        <p className="text-muted-foreground">
          Track and manage customer purchases.
        </p>
      </div>

      <div className="border rounded-md bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Order ID</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Total</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Payment</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell className="font-mono text-xs">{order.id}</TableCell>
                <TableCell>{order.customer}</TableCell>
                <TableCell className="text-xs">{order.date}</TableCell>
                <TableCell>$ {order.total.toFixed(2)}</TableCell>
                <TableCell>
                  <Badge variant="outline" className={getStatusColor(order.status)}>
                    {order.status}
                  </Badge>
                </TableCell>
                <TableCell>
                   <Badge variant={order.payment === "paid" ? "default" : "secondary"}>
                     {order.payment}
                   </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" className="gap-2">
                    <ExternalLink className="h-3 w-3" />
                    Details
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
