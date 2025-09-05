import React, { useEffect, useRef, useState } from 'react';
import { api } from '../api';

type Status = {
  run_id: string;
  status: string;
  progress: number;
  message?: string;
};

export default function RunStatus({
  runId,
  onDone,
}: {
  runId: string;
  onDone?: (ok: boolean) => void;
}) {
  const [s, setS] = useState<Status | null>(null);
  const ivRef = useRef<number>();

  useEffect(() => {
    const tick = async () => {
      const r = await api.get(`/api/runs/${runId}/status`);
      setS(r.data);
      if (r.data.status === 'succeeded' || r.data.status === 'failed') {
        if (ivRef.current) clearInterval(ivRef.current);
        onDone?.(r.data.status === 'succeeded');
      }
    };
    tick();
    ivRef.current = window.setInterval(tick, 900);
    return () => {
      if (ivRef.current) clearInterval(ivRef.current);
    };
  }, [runId]);

  if (!s) return null;

  return (
    <div style={{ marginBottom: 16 }}>
      <div className="label" style={{ marginBottom: 8 }}>
        Status
      </div>
      <div className="progress">
        <div style={{ width: `${s.progress}%` }} />
      </div>
      <div style={{ marginTop: 8, color: 'var(--muted)' }}>
        {s.status} ({s.progress}%)
      </div>
      {s.message && (
        <div style={{ marginTop: 6, color: 'var(--muted)' }}>{s.message}</div>
      )}
    </div>
  );
}