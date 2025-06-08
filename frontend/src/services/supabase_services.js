import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://your-supabase-project-id.supabase.co';
const supabaseKey = 'your-supabase-anon-key';

export const supabase = createClient(supabaseUrl, supabaseKey);