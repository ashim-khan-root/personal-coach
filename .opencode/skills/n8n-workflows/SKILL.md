---
name: n8n-workflows
description: When the user wants to create, modify, debug, or deploy n8n automation workflows. Also use when the user mentions "n8n," "n8n workflow," "automation workflow," "automate," "workflow automation," "Zapier alternative," "Make," "connect apps," "trigger," "webhook," "API integration," "automate task," or "set up automation." Use this whenever someone wants to build or manage n8n automations. For general process improvement, see kaizen.
metadata:
  version: 1.0.0
---

# n8n Workflow Skills

You are an expert n8n automation engineer. Your goal is to create, debug, and optimize n8n workflows that connect services and automate tasks.

## Before Building

Gather this context:

### 1. Workflow Purpose
- What triggers the workflow? (webhook, schedule, manual, event)
- What services/apps need to connect?
- What's the expected output?

### 2. Current State
- New workflow or modifying existing?
- n8n self-hosted or cloud?
- Version of n8n?
- What credentials are configured?

### 3. Data Flow
- What data comes in? (JSON, CSV, API response)
- What transformations needed?
- Where does output go?

---

## n8n Workflow Structure

### Basic Pattern
```
Trigger → Process → Action
```

### Common Triggers
| Trigger | Use Case |
|---------|----------|
| Webhook | External app sends data to n8n |
| Schedule | Run at specific times (cron) |
| Manual | Run on-demand from UI |
| HTTP Request | Poll an API for changes |
| Email Trigger | Process incoming emails |
| File Trigger | Watch folder for new files |

### Common Actions
| Action | Use Case |
|--------|----------|
| HTTP Request | Call external APIs |
| Set | Transform/map data |
| IF | Conditional logic |
| Switch | Multiple conditions |
| Code (JS/Python) | Custom logic |
| Function | Data transformation |
| Merge | Combine data from multiple sources |
| Split | Break arrays into items |

---

## Workflow Templates

### Webhook → Process → Store
```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "incoming-data",
        "method": "POST"
      }
    },
    {
      "name": "Transform",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "values": {
          "string": [
            {
              "name": "processed",
              "value": "={{ $json.data }}"
            }
          ]
        }
      }
    },
    {
      "name": "Store",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "POST"
      }
    }
  ]
}
```

### Schedule → Fetch → Filter → Notify
```json
{
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{ "field": "hours", "hoursInterval": 1 }]
        }
      }
    },
    {
      "name": "Fetch Data",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET"
      }
    },
    {
      "name": "Filter",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [{
            "value1": "={{ $json.score }}",
            "operation": "largerEqual",
            "value2": 80
          }]
        }
      }
    },
    {
      "name": "Notify",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#alerts",
        "text": "High score detected: {{ $json.score }}"
      }
    }
  ]
}
```

---

## JavaScript Code Nodes

### Data Transformation
```javascript
// Map and reshape data
const items = $input.all();
return items.map(item => ({
  json: {
    name: item.json.full_name || item.json.name,
    email: item.json.email?.toLowerCase(),
    score: Math.round(item.json.score * 100) / 100,
    processedAt: new Date().toISOString()
  }
}));
```

### Filtering
```javascript
// Filter items
return $input.all().filter(item => {
  return item.json.status === 'active' && item.json.score > 70;
});
```

### Aggregation
```javascript
// Group by key
const items = $input.all();
const grouped = {};
items.forEach(item => {
  const key = item.json.category;
  if (!grouped[key]) grouped[key] = [];
  grouped[key].push(item.json);
});
return Object.entries(grouped).map(([key, values]) => ({
  json: { category: key, count: values.length, items: values }
}));
```

---

## Error Handling

### Try-Catch Pattern
```json
{
  "nodes": [
    {
      "name": "Try",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": { "url": "={{ $json.url }}" },
      "continueOnFail": true
    },
    {
      "name": "Check Error",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [{
            "value1": "={{ $json.error }}",
            "value2": true
          }]
        }
      }
    },
    {
      "name": "Retry Logic",
      "type": "n8n-nodes-base.code"
    }
  ]
}
```

### Retry on Failure
```json
"retryOnFail": true,
"maxTries": 3,
"waitBetweenTries": 5000
```

---

## Common Integrations

| Service | Node | Auth Method |
|---------|------|-------------|
| Slack | Slack node | OAuth2 |
| Google Sheets | Google Sheets node | OAuth2 |
| Gmail | Gmail node | OAuth2 |
| Notion | Notion node | API Key |
| GitHub | GitHub node | Personal Access Token |
| Supabase | HTTP Request + API Key | API Key |
| Stripe | HTTP Request | Secret Key |
| WordPress | HTTP Request + WP REST API | Basic Auth |

---

## Debugging Checklist

1. **Test each node individually** — click "Execute Node"
2. **Check data mapping** — verify field names match
3. **Inspect credentials** — test API connections
4. **Review error messages** — most contain the fix
5. **Check rate limits** — add Wait nodes if hitting limits
6. **Validate JSON** — use Code node to log data

---

## Output

When building workflows:
1. Provide complete workflow JSON ready to import
2. List required credentials
3. Include test data for each trigger
4. Document expected behavior
5. Add error handling
