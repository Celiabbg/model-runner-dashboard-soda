import React, { useState } from 'react';

type Props = {
  disabled?: boolean;
  onSubmit: (payload: { region: string; year: number; parameter_set: string }) => void;
};

export default function RunForm({ disabled, onSubmit }: Props) {
  const [region, setRegion] = useState('NA');
  const [year, setYear] = useState<number>(2024);
  const [param, setParam] = useState('baseline');

  return (
    <div>
      <div className="row">
        <div className="field">
          <label className="label">Region</label>
          <select
            className="select"
            value={region}
            onChange={e => setRegion(e.target.value)}
          >
            <option>NA</option>
            <option>EMEA</option>
            <option>APAC</option>
          </select>
        </div>
        <div className="field">
          <label className="label">Year</label>
          <input
            className="input"
            type="number"
            value={year}
            onChange={e => setYear(parseInt(e.target.value || '0'))}
          />
        </div>
        <div className="field">
          <label className="label">Parameter Set</label>
          <select
            className="select"
            value={param}
            onChange={e => setParam(e.target.value)}
          >
            <option value="baseline">Baseline</option>
            <option value="optimistic">Optimistic</option>
            <option value="pessimistic">Pessimistic</option>
          </select>
        </div>
      </div>
      <div style={{ marginTop: 14 }}>
        <button
          className="btn primary"
          disabled={disabled}
          onClick={() => onSubmit({ region, year, parameter_set: param })}
        >
          Trigger Run
        </button>
      </div>
    </div>
  );
}