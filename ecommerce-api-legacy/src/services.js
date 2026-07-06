const { Buffer } = require('buffer');
const config = require('./config');
const repo = require('./repositories');

const globalCache = {};

function logAndCache(key, data) {
  console.log(`[LOG] Salvando no cache: ${key}`);
  globalCache[key] = data;
}

function badCrypto(pwd) {
  let hash = '';
  for (let i = 0; i < 10000; i += 1) {
    hash += Buffer.from(pwd).toString('base64').substring(0, 2);
  }
  return hash.substring(0, 10);
}

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
    const hash = badCrypto(pwd || '123456');
    userId = await repo.createUser(usr, eml, hash);
  }

  console.log(`Processando cartão ${card} na chave ${config.paymentGatewayKey}`);
  const paymentStatus = card.startsWith('4') ? 'PAID' : 'DENIED';
  if (paymentStatus === 'DENIED') {
    return { status: 400, body: 'Pagamento recusado' };
  }

  const enrollmentId = await repo.createEnrollment(userId, courseId);
  await repo.createPayment(enrollmentId, course.price, paymentStatus);
  await repo.createAuditLog(`Checkout curso ${courseId} por ${userId}`);
  logAndCache(`last_checkout_${userId}`, course.title);

  return { status: 200, body: { msg: 'Sucesso', enrollment_id: enrollmentId } };
}

async function getFinancialReport() {
  const report = [];
  const courses = await repo.getCourses();

  for (const course of courses) {
    const courseData = { course: course.title, revenue: 0, students: [] };
    const enrollments = await repo.getEnrollmentsByCourse(course.id);

    for (const enrollment of enrollments) {
      const user = await repo.findUserBasicById(enrollment.user_id);
      const payment = await repo.findPaymentByEnrollment(enrollment.id);

      if (payment && payment.status === 'PAID') {
        courseData.revenue += payment.amount;
      }

      courseData.students.push({
        student: user ? user.name : 'Unknown',
        paid: payment ? payment.amount : 0,
      });
    }

    report.push(courseData);
  }

  return report;
}

async function deleteUserAndKeepAudit(id) {
  await repo.deleteUser(id);
  return 'Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.';
}

module.exports = {
  processCheckout,
  getFinancialReport,
  deleteUserAndKeepAudit,
  logAndCache,
  badCrypto,
  globalCache,
};

