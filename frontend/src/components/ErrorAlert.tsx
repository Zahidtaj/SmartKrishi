import { AlertCircle } from "lucide-react";

interface ErrorAlertProps {
  title?: string;
  message: string;
}

export function ErrorAlert({ title, message }: ErrorAlertProps) {
  return (
    <div
      role="alert"
      className="flex items-start gap-3 rounded-lg border border-danger/45 bg-danger/10 p-4 text-sm text-ink"
    >
      <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-danger" aria-hidden="true" />
      <div>
        {title && <p className="font-semibold text-danger">{title}</p>}
        <p className="text-ink/90">{message}</p>
      </div>
    </div>
  );
}
