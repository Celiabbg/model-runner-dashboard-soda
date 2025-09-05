import React from 'react';

type Props = {
  models: { id: string; name: string }[];
  value: string;
  onChange: (id: string) => void;
};

export default function ModelSelector({ models, value, onChange }: Props) {
  return (
    <div className="field" style={{ marginBottom: 10 }}>
      <label className="label">Select a Model</label>
      <select
        className="select"
        value={value}
        onChange={e => onChange(e.target.value)}
      >
        <option value="" disabled>
          Select…
        </option>
        {models.map(m => (
          <option key={m.id} value={m.id}>
            {m.name}
          </option>
        ))}
      </select>
    </div>
  );
}