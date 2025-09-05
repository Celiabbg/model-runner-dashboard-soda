import React, { useEffect, useRef, useState } from 'react';
import { api } from '../api';

type Row = Record<string, string | number>;

export default function ResultsTable({
  runId,
  active,
}: {
  runId: string;
  active: boolean;
}) {
  const [rows, setRows] = useState<Row[]>([]);
  const [summary, setSummary] = useState<Record<string, number>>({});
  const [error, setError] = useState('');
  const loadedRef = useRef(false);

  useEffect(() => {
    loadedRef.current = false;
    setRows([]);
    setSummary({});
    setError('');
  }, [runId]);

  useEffect(() => {
    if (!active || loadedRef.current) return;
    const load = async () => {
      try {
        const r = await api.get(`/api/runs/${runId}/results`);
        setRows(r.data.rows || []);
        setSummary(r.data.summary || {});
        loadedRef.current = true;
      } catch (e: any) {
        setError(e.message || 'No data yet');
      }
    };
    load();
  }, [active, runId]);

  if (error)
    return (
      <div className="error-banner" style={{ marginTop: 10 }}>
        {error}
      </div>
    );
  if (!rows.length)
    return <div style={{ color: 'var(--muted)' }}>No results yet.</div>;

  const headers = Object.keys(rows[0] || {});

  return (
    <div>
      <div className="kpis" style={{ marginBottom: 12 }}>
        {Object.entries(summary).map(([k, v]) => (
          <div className="kpi" key={k}>
            <div className="label" style={{ marginBottom: 4 }}>
              {k}
            </div>
            <div className="v">{v}</div>
          </div>
        ))}
      </div>

      <div className="table-wrap">
        <table className="table">
          <thead>
            <tr>
              {headers.map(h => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                {headers.map(h => (
                  <td key={h}>{String(r[h] ?? '')}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}