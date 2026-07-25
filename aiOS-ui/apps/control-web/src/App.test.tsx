import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { App } from './App';

describe('App', () => {
  it('opens the agent and tools control surface from the navigation', () => {
    vi.stubGlobal('fetch', vi.fn((path: string) => Promise.resolve(new Response(JSON.stringify(
      path === '/api/extensions' ? { extensions: [] } : { agents: [] }
    )) as Response)));

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: 'Agents & Tools' }));

    expect(screen.getByRole('heading', { name: 'Agents & Tools' })).toBeTruthy();
  });
});
