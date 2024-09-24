interface Task {
  pk: number
  parent?: number
  name: string
  description: string
  status: number
  assignee?: number
  due_date?: string
  _due_date?: Date
  priority: number
  created: string
  updated: string
}

interface Status {
  pk: number
  name: string
  description: string
  order: number
  color: string
}

interface User {
  pk: number
  username: string
  email: string
  first_name: string
  last_name: string
}

const priorities = [
  {
    title: 'Low',
    value: -1,
    color: 'grey',
  },
  {
    title: 'Normal',
    value: 0,
    color: '--var(--v-primary)',
  },
  {
    title: 'Medium',
    value: 1,
    color: 'green',
  },
  {
    title: 'High',
    value: 2,
    color: 'orange',
  },
  {
    title: 'Red Hot',
    value: 5,
    color: 'red',
  },
]

export type { Task, Status, User }
export { priorities }
