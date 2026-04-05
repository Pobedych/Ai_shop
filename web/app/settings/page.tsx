import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">
          Configure your bot and dashboard preferences.
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Bot Configuration</CardTitle>
            <CardDescription>
              General settings for your Telegram bot.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="bot-name">Bot Display Name</Label>
              <Input id="bot-name" defaultValue="Ai-shop Bot" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="welcome-msg">Welcome Message</Label>
              <Input id="welcome-msg" defaultValue="Welcome to our shop!" />
            </div>
            <Button>Save Changes</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>API Access</CardTitle>
            <CardDescription>
              Manage API keys and external integrations.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="api-key">Admin API Key</Label>
              <div className="flex gap-2">
                <Input id="api-key" value="test_key_hidden" readOnly />
                <Button variant="outline">Regenerate</Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Danger Zone</CardTitle>
            <CardDescription>
              Irreversible actions for your shop.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button variant="destructive">Reset Shop Data</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
