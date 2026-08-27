const repo = require('./repositories');
const { hashPassword } = require('./utils');

async function processCheckout({ usr, eml, pwd, c_id: courseId, card }) {
  if (!usr || !eml || !courseId || !card) {
    return { status: 400, body: 'Bad Request' };
  }

  const course = await repo.findCourseById(courseId);
  if (!course) {
    return { status: 404, body: 'Curso não encontrado' };
  }

  let user = await repo.findUserByEmail(eml);
  let userId = user && user.id;

  if (!userId) {
    if (!pwd) {
      return { status: 400, body: 'Senha obrigatoria' };
    }
    const hash = hashPassword(pwd);
    userId = await repo.createUser(usr, eml, hash);
  }

  console.info('Checkout em processamento', { userId, courseId });
  const paymentStatus = card.startsWith('4') ? 'PAID' : 'DENIED';
  if (paymentStatus === 'DENIED') {
    return { status: 400, body: 'Pagamento recusado' };
  }

  const enrollmentId = await repo.createEnrollment(userId, courseId);
  await repo.createPayment(enrollmentId, course.price, paymentStatus);
  await repo.createAuditLog(`Checkout curso ${courseId} por ${userId}`);

  return { status: 200, body: { msg: 'Sucesso', enrollment_id: enrollmentId } };
}

async function getFinancialReport() {
  const reportByCourse = new Map();
  const rows = await repo.getFinancialReportRows();

  for (const row of rows) {
    let course = reportByCourse.get(row.course_id);
    if (!course) {
      course = { course: row.course_title, revenue: 0, students: [] };
      reportByCourse.set(row.course_id, course);
    }

    if (row.enrollment_id === null) continue;

    const paid = row.payment_amount ?? 0;
    if (row.payment_status === 'PAID') {
      course.revenue += paid;
    }

    course.students.push({
      student: row.user_name || 'Unknown',
      paid,
    });
  }

  return [...reportByCourse.values()];
}

async function deleteUserAndKeepAudit(id) {
  await repo.deleteUser(id);
  return 'Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.';
}

module.exports = {
  processCheckout,
  getFinancialReport,
  deleteUserAndKeepAudit,
};
