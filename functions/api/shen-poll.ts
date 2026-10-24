/**
 * Cloudflare Pages Functions: functions/api/shen-poll.ts
 * Dashboard -> Pages -> Settings -> Functions -> D1 bindings: DB -> your D1 database.
 * Stores a random per-browser UUID and choice; no IP/email persisted.
 */
type Row = { choice: string; votes: number };
type Query = {bind: (...values: unknown[]) => Query; run: () => Promise<unknown>; all: () => Promise<{results: Row[]}>};
type Db = {prepare: (sql: string) => Query};
type Context = {env: {DB?: Db}; request: Request};

const allowed = new Set(['A','B','C','D']);
const json = (data: unknown, status=200) => new Response(JSON.stringify(data),{
  status, headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff'},
});

async function counts(db:Db){
  const {results}=await db.prepare('SELECT choice, COUNT(*) AS votes FROM shen_poll_votes GROUP BY choice').all();
  const grouped:Record<string,number>={A:0,B:0,C:0,D:0};
  for(const row of results){if(allowed.has(row.choice))grouped[row.choice]=Number(row.votes);}
  return {counts:grouped,total:Object.values(grouped).reduce((a,b)=>a+b,0)};
}

export async function onRequestGet({env}:Context){
  if(!env.DB)return json({error:'D1 binding DB not configured'},503);
  try{return json(await counts(env.DB));}
  catch{return json({error:'Database temporarily unavailable'},503);}
}

export async function onRequestPost({env,request}:Context){
  if(!env.DB)return json({error:'D1 binding DB not configured'},503);
  const contentType=request.headers.get('content-type')||'';
  if(!contentType.startsWith('application/json'))return json({error:'JSON only'},415);
  const declared=Number(request.headers.get('content-length')||0);
  if(declared>1024)return json({error:'Payload too large'},413);
  let payload:any;
  try{payload=await request.json();}catch{return json({error:'Invalid JSON'},400);}
  const choice=payload?.choice, voterId=payload?.voterId;
  if(typeof choice!=='string'||!allowed.has(choice))return json({error:'Invalid choice'},400);
  if(typeof voterId!=='string'||!/^[-0-9a-f]{36}$/i.test(voterId))return json({error:'Invalid browser ID'},400);
  try{
    await env.DB.prepare('INSERT INTO shen_poll_votes(voter_id,choice) VALUES(?,?) ON CONFLICT(voter_id) DO UPDATE SET choice=excluded.choice, updated_at=CURRENT_TIMESTAMP').bind(voterId,choice).run();
    return json(await counts(env.DB));
  }catch{return json({error:'Database temporarily unavailable'},503);}
}
