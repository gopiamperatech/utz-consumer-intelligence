import React, { useEffect, useMemo, useState } from 'react';
import {
  Search,
  MessageSquare,
  MapPin,
  Store,
  AlertTriangle,
  TrendingUp,
  Sparkles,
  Activity,
  Bot,
  ArrowRight,
  Package,
  Brain,
  RefreshCw,
} from 'lucide-react';
import { BarChart, Bar, CartesianGrid, LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api } from './api';

const COLORS = ['#0f172a', '#334155', '#64748b', '#94a3b8', '#cbd5e1', '#e2e8f0'];

function ShellCard({ children, className = '' }) {
  return <div className={`card ${className}`}>{children}</div>;
}

function MetricCard({ item }) {
  return (
    <ShellCard>
      <div className="metric-topline">{item.title}</div>
      <div className="metric-value-row">
        <div className="metric-value">{item.value}</div>
        <div className="metric-delta">{item.delta}</div>
      </div>
      <div className="metric-note">{item.note}</div>
    </ShellCard>
  );
}

function QueryPill({ children, tone = 'neutral' }) {
  return <span className={`pill pill-${tone}`}>{children}</span>;
}

function QueryCard({ item }) {
  const sentimentTone = item.sentiment === 'Negative' ? 'red' : item.sentiment === 'Positive' ? 'green' : 'neutral';
  const priorityTone = item.priority === 'High' ? 'amber' : item.priority === 'Medium' ? 'blue' : 'neutral';

  return (
    <div className="query-card">
      <div className="query-toprow">
        <div className="query-text">{item.text}</div>
        <div className="query-time">{item.timestamp_label}</div>
      </div>
      <div className="query-pills">
        <QueryPill>{item.intent}</QueryPill>
        <QueryPill>{item.product}</QueryPill>
        <QueryPill tone={sentimentTone}>{item.sentiment}</QueryPill>
        <QueryPill tone={priorityTone}>{item.priority}</QueryPill>
      </div>
      <div className="query-meta-row">
        <span><MessageSquare size={14} />{item.channel}</span>
        <span><MapPin size={14} />{item.location}</span>
        <span><Store size={14} />{item.retailer}</span>
      </div>
    </div>
  );
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [queries, setQueries] = useState([]);
  const [gaps, setGaps] = useState({ gaps: [], trend: [], intent_distribution: [] });
  const [actions, setActions] = useState([]);
  const [search, setSearch] = useState('');
  const [channel, setChannel] = useState('all');
  const [activeTab, setActiveTab] = useState('signals');
  const [copilotPrompt, setCopilotPrompt] = useState('What are consumers struggling with this week?');
  const [copilotAnswer, setCopilotAnswer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [error, setError] = useState('');

  async function loadAll() {
    try {
      setLoading(true);
      setError('');
      const [summaryRes, queryRes, gapsRes, actionsRes] = await Promise.all([
        api.getSummary(),
        api.getQueries({ search, channel }),
        api.getGaps(),
        api.getActions(),
      ]);
      setSummary(summaryRes);
      setQueries(queryRes.items || []);
      setGaps(gapsRes);
      setActions(actionsRes.items || []);
    } catch (err) {
      setError(err.message || 'Failed to load prototype data');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const timeout = setTimeout(async () => {
      try {
        const queryRes = await api.getQueries({ search, channel });
        setQueries(queryRes.items || []);
      } catch (err) {
        setError(err.message || 'Failed to refresh queries');
      }
    }, 250);
    return () => clearTimeout(timeout);
  }, [search, channel]);

  async function runCopilot(prompt) {
    try {
      setCopilotLoading(true);
      setCopilotPrompt(prompt);
      const response = await api.askCopilot(prompt);
      setCopilotAnswer(response);
      setActiveTab('copilot');
    } catch (err) {
      setError(err.message || 'Copilot request failed');
    } finally {
      setCopilotLoading(false);
    }
  }

  const executivePulse = summary?.executive_pulse;
  const kpis = summary?.kpis || [];

  const topSignalsText = useMemo(() => {
    if (!gaps.gaps.length) return 'Demand friction is clustering around product discovery.';
    return `${gaps.gaps[0].region} currently shows the highest demand-friction concentration.`;
  }, [gaps.gaps]);

  return (
    <div className="page">
      <div className="container">
        <div className="hero card hero-card">
          <div className="hero-grid">
            <div>
              <div className="eyebrow"><Sparkles size={14} /> Consumer Intent Intelligence Platform</div>
              <h1>Convert consumer conversations into measurable demand actions.</h1>
              <p>
                Prototype for Utz Brands that turns search, chat, reviews, and consumer feedback into
                findability insights, retail-gap detection, and brand-marketing recommendations.
              </p>
              <div className="hero-actions">
                <button className="btn btn-primary" onClick={() => setActiveTab('signals')}>View live signals</button>
                <button className="btn btn-secondary" onClick={() => runCopilot('Give me an executive summary')}>Open brand copilot</button>
              </div>
            </div>
            <div className="pulse-panel">
              <div className="pulse-title"><Activity size={16} /> Executive Pulse</div>
              <div className="pulse-item">
                <div className="label">Top friction theme</div>
                <div className="value">{executivePulse?.top_friction_theme || 'Loading...'}</div>
              </div>
              <div className="pulse-item">
                <div className="label">Most affected markets</div>
                <div className="value">{executivePulse?.affected_markets?.join(', ') || 'Loading...'}</div>
              </div>
              <div className="pulse-item">
                <div className="label">Most affected products</div>
                <div className="value">{executivePulse?.affected_products?.join(', ') || 'Loading...'}</div>
              </div>
              <div className="pulse-item">
                <div className="label">Immediate action</div>
                <div className="value">{executivePulse?.immediate_action || 'Loading...'}</div>
              </div>
            </div>
          </div>
        </div>

        {error ? <div className="error-banner">{error}</div> : null}

        <div className="metric-grid">
          {kpis.map((item) => <MetricCard key={item.title} item={item} />)}
        </div>

        <div className="tabs-row">
          {[
            ['signals', 'Consumer Signals'],
            ['gaps', 'Demand Gaps'],
            ['actions', 'Action Engine'],
            ['copilot', 'Brand Copilot'],
          ].map(([key, label]) => (
            <button key={key} className={`tab-btn ${activeTab === key ? 'active' : ''}`} onClick={() => setActiveTab(key)}>
              {label}
            </button>
          ))}
          <button className="refresh-btn" onClick={loadAll}><RefreshCw size={15} /> Refresh</button>
        </div>

        {loading ? <div className="loading-card card">Loading prototype data...</div> : null}

        {!loading && activeTab === 'signals' && (
          <div className="section-grid section-grid-signals">
            <ShellCard>
              <div className="section-header">
                <div>
                  <div className="section-title">Live consumer conversation feed</div>
                  <div className="section-subtitle">Search, chat, social, review, and contact-center signals transformed into structured intent.</div>
                </div>
              </div>
              <div className="filters-row">
                <div className="input-wrap">
                  <Search size={16} />
                  <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search by query, product, intent, or location"
                  />
                </div>
                <select value={channel} onChange={(e) => setChannel(e.target.value)}>
                  <option value="all">All channels</option>
                  <option value="Website Search">Website Search</option>
                  <option value="Chatbot">Chatbot</option>
                  <option value="Review">Review</option>
                  <option value="Social">Social</option>
                  <option value="Contact Center">Contact Center</option>
                </select>
              </div>
              <div className="query-list">
                {queries.map((item) => <QueryCard key={item.id} item={item} />)}
              </div>
            </ShellCard>

            <div className="side-stack">
              <ShellCard>
                <div className="section-title">Intent distribution</div>
                <div className="section-subtitle">Where consumer attention is clustering right now.</div>
                <div className="chart-wrap medium">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={gaps.intent_distribution} dataKey="value" nameKey="name" innerRadius={55} outerRadius={92}>
                        {gaps.intent_distribution.map((entry, index) => (
                          <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </ShellCard>

              <ShellCard>
                <div className="section-title">Top opportunity signal</div>
                <div className="section-subtitle">{topSignalsText}</div>
                <div className="highlight-box">
                  <div className="highlight-row">
                    <div>
                      <div className="label">Store-locator assisted conversion opportunity</div>
                      <div className="highlight-value">+8.5% potential lift</div>
                    </div>
                    <TrendingUp size={24} />
                  </div>
                  <div className="progress-bar"><span style={{ width: '72%' }} /></div>
                  <div className="metric-note">
                    Consumers already express intent. The gap is not demand generation — it is helping them find the
                    right product at the right retailer.
                  </div>
                </div>
              </ShellCard>
            </div>
          </div>
        )}

        {!loading && activeTab === 'gaps' && (
          <div className="section-grid section-grid-gaps">
            <ShellCard>
              <div className="section-title">Findability and demand-gap hotspots</div>
              <div className="section-subtitle">Regional concentration of demand friction versus brand opportunity.</div>
              <div className="chart-wrap large">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={gaps.gaps}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="region" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="gap" radius={[8, 8, 0, 0]} />
                    <Bar dataKey="opportunity" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </ShellCard>

            <ShellCard>
              <div className="section-title">Weekly friction trend</div>
              <div className="section-subtitle">Rising findability issues are pulling up out-of-stock mentions.</div>
              <div className="chart-wrap large">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={gaps.trend}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="findability" stroke="#0f172a" strokeWidth={3} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="outOfStock" stroke="#64748b" strokeWidth={3} dot={{ r: 4 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </ShellCard>
          </div>
        )}

        {!loading && activeTab === 'actions' && (
          <ShellCard>
            <div className="section-title"><ArrowRight size={18} /> Conversation-to-action engine</div>
            <div className="section-subtitle">Translate consumer patterns into marketing, retail, and content actions.</div>
            <div className="actions-grid">
              {actions.map((row) => (
                <div key={row.id} className="action-row">
                  <div>
                    <div className="small-label">Consumer pattern</div>
                    <div className="strong-text">{row.pattern}</div>
                  </div>
                  <div>
                    <div className="small-label">Evidence</div>
                    <div className="body-text">{row.evidence}</div>
                  </div>
                  <div>
                    <div className="small-label">Recommended action</div>
                    <div className="body-text emphasis">{row.action}</div>
                  </div>
                  <div>
                    <div className="small-label">Owner</div>
                    <QueryPill>{row.owner}</QueryPill>
                  </div>
                  <div>
                    <div className="small-label">Impact</div>
                    <QueryPill tone={row.impact === 'High' ? 'green' : 'blue'}>{row.impact}</QueryPill>
                  </div>
                </div>
              ))}
            </div>
          </ShellCard>
        )}

        {!loading && activeTab === 'copilot' && (
          <div className="section-grid section-grid-copilot">
            <ShellCard>
              <div className="section-title"><Bot size={18} /> Brand marketing copilot</div>
              <div className="section-subtitle">Natural-language layer for strategic and self-service analytics.</div>
              <div className="prompt-buttons">
                {[
                  'What are consumers struggling with this week?',
                  'What campaign should the brand team launch next?',
                  'Give me an executive summary',
                ].map((prompt) => (
                  <button
                    key={prompt}
                    className={`prompt-btn ${copilotPrompt === prompt ? 'active' : ''}`}
                    onClick={() => runCopilot(prompt)}
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </ShellCard>

            <ShellCard>
              <div className="section-title"><Brain size={18} /> AI response</div>
              <div className="section-subtitle">LLM-driven explanation layer over structured and unstructured consumer signals.</div>
              <div className="copilot-box">
                {copilotLoading ? (
                  <div className="body-text">Generating response...</div>
                ) : copilotAnswer ? (
                  <>
                    <div className="copilot-answer">{copilotAnswer.answer}</div>
                    <div className="copilot-source">Source: {copilotAnswer.source}</div>
                    <div className="supporting-list">
                      {copilotAnswer.supporting_points?.map((point, idx) => (
                        <div key={`${point}-${idx}`} className="supporting-item">
                          <Package size={14} />
                          <span>{point}</span>
                        </div>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="body-text">Run one of the prompts to see the copilot response.</div>
                )}
              </div>
            </ShellCard>
          </div>
        )}
      </div>
    </div>
  );
}
