
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

export default function AzureCostOptimizer() {
  const [subscriptionId, setSubscriptionId] = useState("");
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGeneratePrompt = async () => {
    setLoading(true);
    try {
      const response = await fetch("https://costopt-api-app.azurewebsites.net/api/generate-prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ subscriptionId }),
      });
      const data = await response.json();
      setPrompt(data.prompt);
    } catch (error) {
      setPrompt("Error generating prompt. Please check console for details.");
      console.error("Prompt generation error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <Card>
        <CardContent className="space-y-4">
          <h2 className="text-xl font-semibold">Azure Cost Optimizer</h2>
          <Input
            placeholder="Enter Azure Subscription ID"
            value={subscriptionId}
            onChange={(e) => setSubscriptionId(e.target.value)}
          />
          <Button onClick={handleGeneratePrompt} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2 h-4 w-4" /> Generating...
              </>
            ) : (
              "Generate Cost Optimization Prompt"
            )}
          </Button>
          <Textarea
            value={prompt}
            className="h-60"
            readOnly
            placeholder="Generated prompt will appear here"
          />
        </CardContent>
      </Card>
    </div>
  );
}
